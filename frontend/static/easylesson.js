const fileTree = document.getElementById('file-tree');
const splitter = document.querySelector('.splitter');
const leftPanel = document.querySelector('.left-panel');
const rightPanel = document.querySelector('.right-panel');
const fileInput = document.getElementById('file-input');
const folderInput = document.getElementById('folder-input');
const fileDropZone = document.getElementById('file-drop-zone');
const uploadFileBtn = document.getElementById('upload-file-btn');
const uploadFolderBtn = document.getElementById('upload-folder-btn');
const newFolderNameInput = document.getElementById('new-folder-name');
const parentFolderSelect = document.getElementById('parent-folder-select');
const createFolderBtn = document.getElementById('create-folder-btn');
const statusMessages = document.getElementById('status-messages');
const selectedFileInfo = document.getElementById('selected-file-info');
const selectedFolderInfo = document.getElementById('selected-folder-info');

let currentTreeData = {};
let currentSelectedPath = ''; // Track the currently selected file/folder path
let currentSelectedFile = null; // Track the selected file for upload
let currentSelectedFolder = null; // Track the selected folder for upload

// Helper to display status messages
function displayStatus(message, type) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add(`status-${type}`);
    msgDiv.textContent = `${new Date().toLocaleTimeString()}: ${message}`;
    statusMessages.prepend(msgDiv); // Add to top
    // Auto-remove after some time
    setTimeout(() => msgDiv.remove(), 7000);
}

// Fetch and render directory tree
async function fetchDirectoryTree() {
    fileTree.innerHTML = '<div class="loading">Loading file tree...</div>';
    try {
        const response = await fetch('/api/directory-tree');
        const data = await response.json();
        if (data.success) {
            currentTreeData = data.tree;
            renderFileTree(currentTreeData, fileTree, data.path);
            updateParentFolderSelect(currentTreeData, data.path);
        } else {
            displayStatus(`Error fetching directory tree: ${data.message}`, 'error');
            fileTree.innerHTML = '<div class="error">Failed to load file tree.</div>';
        }
    } catch (error) {
        displayStatus(`Network error fetching directory tree: ${error.message}`, 'error');
        fileTree.innerHTML = '<div class="error">Network error.</div>';
    }
}

function renderFileTree(items, parentElement, basePath, level = 0) {
    parentElement.innerHTML = ''; // Clear existing tree
    items.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.classList.add('tree-item');
        itemElement.dataset.path = item.path;
        itemElement.dataset.type = item.type;
        itemElement.style.paddingLeft = `${level * 10 + 8}px`; // Indent based on level

        const icon = document.createElement('span');
        icon.classList.add('icon');
        icon.classList.add(item.type === 'folder' ? 'folder-icon' : 'file-icon');
        itemElement.appendChild(icon);

        const nameSpan = document.createElement('span');
        nameSpan.textContent = item.name;
        itemElement.appendChild(nameSpan);

        if (item.type === 'folder') {
            itemElement.classList.add('collapsed'); // Start collapsed
            itemElement.addEventListener('click', (event) => {
                if (event.target === nameSpan || event.target === icon) { // Only toggle if name or icon clicked
                    itemElement.classList.toggle('expanded');
                    itemElement.classList.toggle('collapsed');
                    const contents = itemElement.querySelector('.folder-contents');
                    if (contents) {
                        contents.style.display = itemElement.classList.contains('expanded') ? 'block' : 'none';
                    } else {
                        // Dynamically render children if not already present
                        const newContents = document.createElement('div');
                        newContents.classList.add('folder-contents');
                        itemElement.appendChild(newContents);
                        renderFileTree(item.children, newContents, basePath, level + 1);
                    }
                }
                selectItem(itemElement);
            });
            // Initial render for children (hidden)
            if (item.children && item.children.length > 0) {
                const contents = document.createElement('div');
                contents.classList.add('folder-contents');
                contents.style.display = 'none'; // Hidden by default
                itemElement.appendChild(contents);
                // Children will be rendered on expand
            }
        } else { // File
            itemElement.addEventListener('click', () => selectItem(itemElement));
        }
        parentElement.appendChild(itemElement);
    });
}


function selectItem(itemElement) {
    // Remove 'selected' from previously selected item
    const previouslySelected = document.querySelector('.tree-item.selected');
    if (previouslySelected) {
        previouslySelected.classList.remove('selected');
    }
    // Add 'selected' to the clicked item
    itemElement.classList.add('selected');
    currentSelectedPath = itemElement.dataset.path;
}

function updateParentFolderSelect(tree, basePath, currentPath = '') {
    parentFolderSelect.innerHTML = '';
    const rootOption = document.createElement('option');
    rootOption.value = basePath;
    rootOption.textContent = 'EasyLessonPlan (Root)';
    parentFolderSelect.appendChild(rootOption);

    function addFoldersToSelect(nodes, currentPathPrefix = '') {
        nodes.forEach(node => {
            if (node.type === 'folder') {
                const fullPath = `${currentPathPrefix}/${node.name}`.replace('//', '/');
                const option = document.createElement('option');
                option.value = node.path;
                option.textContent = `/${node.path}`;
                parentFolderSelect.appendChild(option);
                if (node.children) {
                    addFoldersToSelect(node.children, fullPath);
                }
            }
        });
    }
    addFoldersToSelect(tree, '');
}

// Resizable splitter logic
let isResizing = false;
splitter.addEventListener('mousedown', (e) => {
    isResizing = true;
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
});

function handleMouseMove(e) {
    if (!isResizing) return;
    const containerWidth = splitter.parentElement.offsetWidth;
    let newLeftWidth = (e.clientX / containerWidth) * 100;

    // Constrain resizing
    newLeftWidth = Math.max(20, Math.min(50, newLeftWidth)); // Min 20%, Max 50%

    leftPanel.style.width = `${newLeftWidth}%`;
    rightPanel.style.width = `${100 - newLeftWidth}%`;
}

function handleMouseUp() {
    isResizing = false;
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
}

// File Upload
fileInput.addEventListener('change', (e) => {
    currentSelectedFile = e.target.files[0];
    if (currentSelectedFile) {
        selectedFileInfo.textContent = `Selected File: ${currentSelectedFile.name} (${(currentSelectedFile.size / 1024).toFixed(2)} KB)`;
        uploadFileBtn.disabled = false;
    } else {
        selectedFileInfo.textContent = '';
        uploadFileBtn.disabled = true;
    }
});

fileDropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileDropZone.classList.add('highlight');
});

fileDropZone.addEventListener('dragleave', () => {
    fileDropZone.classList.remove('highlight');
});

fileDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    fileDropZone.classList.remove('highlight');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files; // Assign files to the input for consistent handling
        fileInput.dispatchEvent(new Event('change'));
    }
});

uploadFileBtn.addEventListener('click', async () => {
    if (!currentSelectedFile) {
        displayStatus('No file selected for upload.', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('file', currentSelectedFile);
    formData.append('parent_folder', currentSelectedPath || parentFolderSelect.value); // Use selected path or default

    displayStatus(`Uploading file: ${currentSelectedFile.name}...`, 'info');
    uploadFileBtn.disabled = true;

    try {
        const response = await fetch('/api/upload-file', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        if (data.success) {
            displayStatus(`Successfully uploaded file: ${currentSelectedFile.name}`, 'success');
            currentSelectedFile = null;
            selectedFileInfo.textContent = '';
            uploadFileBtn.disabled = true;
            fetchDirectoryTree(); // Refresh tree
        } else {
            displayStatus(`Error uploading file: ${data.message}`, 'error');
        }
    } catch (error) {
        displayStatus(`Network error uploading file: ${error.message}`, 'error');
    } finally {
        uploadFileBtn.disabled = false;
    }
});

// Folder Upload
folderInput.addEventListener('change', (e) => {
    const files = e.target.files;
    if (files.length > 0) {
        currentSelectedFolder = files;
        let folderName = '';
        if (files[0].webkitRelativePath) {
            folderName = files[0].webkitRelativePath.split('/')[0];
        } else {
            folderName = 'Selected Folder'; // Fallback
        }
        selectedFolderInfo.textContent = `Selected Folder: ${folderName} (${files.length} items)`;
        uploadFolderBtn.disabled = false;
    } else {
        currentSelectedFolder = null;
        selectedFolderInfo.textContent = '';
        uploadFolderBtn.disabled = true;
    }
});

uploadFolderBtn.addEventListener('click', async () => {
    if (!currentSelectedFolder || currentSelectedFolder.length === 0) {
        displayStatus('No folder selected for upload.', 'error');
        return;
    }

    const formData = new FormData();
    let rootFolderName = '';
    if (currentSelectedFolder[0].webkitRelativePath) {
        rootFolderName = currentSelectedFolder[0].webkitRelativePath.split('/')[0];
    } else {
        displayStatus('Unable to determine root folder name for upload.', 'error');
        return;
    }

    formData.append('folder_name', rootFolderName);
    formData.append('parent_folder', currentSelectedPath || parentFolderSelect.value);

    for (let i = 0; i < currentSelectedFolder.length; i++) {
        const file = currentSelectedFolder[i];
        const relativePath = file.webkitRelativePath.substring(rootFolderName.length + 1); // Path relative to the root folder
        formData.append('files[]', file, file.name); // Append file
        formData.append(`paths[${file.name}]`, relativePath); // Append its relative path
    }

    displayStatus(`Uploading folder: ${rootFolderName} with ${currentSelectedFolder.length} items...`, 'info');
    uploadFolderBtn.disabled = true;

    try {
        const response = await fetch('/api/upload-folder', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        if (data.success) {
            displayStatus(`Successfully uploaded folder: ${rootFolderName}`, 'success');
            currentSelectedFolder = null;
            selectedFolderInfo.textContent = '';
            uploadFolderBtn.disabled = true;
            fetchDirectoryTree(); // Refresh tree
        } else {
            displayStatus(`Error uploading folder: ${data.message}`, 'error');
        }
    } catch (error) {
        displayStatus(`Network error uploading folder: ${error.message}`, 'error');
    } finally {
        uploadFolderBtn.disabled = false;
    }
});

// Create Folder
createFolderBtn.addEventListener('click', async () => {
    const folderName = newFolderNameInput.value.trim();
    if (!folderName) {
        displayStatus('Folder name cannot be empty.', 'error');
        return;
    }

    const parentFolder = parentFolderSelect.value;

    displayStatus(`Creating folder: ${folderName} in ${parentFolder}...`, 'info');
    createFolderBtn.disabled = true;

    try {
        const response = await fetch('/api/create-folder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ folder_name: folderName, parent_folder: parentFolder }),
        });
        const data = await response.json();
        if (data.success) {
            displayStatus(`Successfully created folder: ${folderName}`, 'success');
            newFolderNameInput.value = '';
            fetchDirectoryTree(); // Refresh tree
        } else {
            displayStatus(`Error creating folder: ${data.message}`, 'error');
        }
    } catch (error) {
        displayStatus(`Network error creating folder: ${error.message}`, 'error');
    } finally {
        createFolderBtn.disabled = false;
    }
});

// Context Menu (Right-click)
fileTree.addEventListener('contextmenu', (e) => {
    const targetItem = e.target.closest('.tree-item');
    if (targetItem && targetItem.dataset.type === 'folder') {
        e.preventDefault();
        selectItem(targetItem); // Select the folder that was right-clicked

        const contextMenu = document.createElement('div');
        contextMenu.classList.add('context-menu');
        contextMenu.style.left = `${e.clientX}px`;
        contextMenu.style.top = `${e.clientY}px`;

        const createFolderOption = document.createElement('div');
        createFolderOption.classList.add('context-menu-item');
        createFolderOption.textContent = 'Create New Folder Here';
        createFolderOption.addEventListener('click', () => {
            newFolderNameInput.focus();
            parentFolderSelect.value = targetItem.dataset.path;
            contextMenu.remove();
        });
        contextMenu.appendChild(createFolderOption);

        const uploadFileOption = document.createElement('div');
        uploadFileOption.classList.add('context-menu-item');
        uploadFileOption.textContent = 'Upload File Here';
        uploadFileOption.addEventListener('click', () => {
            fileInput.click();
            parentFolderSelect.value = targetItem.dataset.path;
            contextMenu.remove();
        });
        contextMenu.appendChild(uploadFileOption);

        const uploadFolderOption = document.createElement('div');
        uploadFolderOption.classList.add('context-menu-item');
        uploadFolderOption.textContent = 'Upload Folder Here';
        uploadFolderOption.addEventListener('click', () => {
            folderInput.click();
            parentFolderSelect.value = targetItem.dataset.path;
            contextMenu.remove();
        });
        contextMenu.appendChild(uploadFolderOption);

        document.body.appendChild(contextMenu);

        // Close context menu when clicking elsewhere
        document.addEventListener('click', () => contextMenu.remove(), { once: true });
    }
});


// Initial load
document.addEventListener('DOMContentLoaded', fetchDirectoryTree);
