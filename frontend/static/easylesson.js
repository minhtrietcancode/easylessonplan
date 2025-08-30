// ===== EASYLESSON APP - MODULAR JAVASCRIPT =====

// ===== APP INITIALIZATION =====
class EasyLessonApp {
    constructor() {
        this.elements = this.initializeElements();
        this.resizer = new ColumnResizer(this.elements.container);
        this.chatInterface = new ChatInterface(this.elements.chat);
        this.fileUploader = new FileUploader(this.elements.upload);
        
        this.init();
    }

    initializeElements() {
        return {
            container: document.getElementById('mainContainer'),
            leftColumn: document.getElementById('leftColumn'),
            middleColumn: document.getElementById('middleColumn'),
            rightColumn: document.getElementById('rightColumn'),
            chat: {
                container: document.getElementById('chatContainer'),
                messagesArea: document.getElementById('messagesArea'),
                messageInput: document.getElementById('messageInput'),
                sendButton: document.getElementById('sendButton'),
                inputArea: document.getElementById('inputArea')
            },
            upload: {
                button: document.getElementById('uploadButton'),
                displayArea: document.getElementById('fileDisplayArea')
            }
        };
    }

    init() {
        console.log('EasyLesson App Initialized');
        
        // Handle window resize
        window.addEventListener('resize', () => {
            this.chatInterface.adjustLayout();
        });
    }
}

// ===== COLUMN RESIZER MODULE =====
class ColumnResizer {
    constructor(container) {
        this.container = container;
        this.isResizing = false;
        this.currentResizer = null;
        this.startX = 0;
        this.startWidths = [];
        
        this.init();
    }

    init() {
        const resizers = this.container.querySelectorAll('.resizer');
        
        resizers.forEach((resizer) => {
            resizer.addEventListener('mousedown', (e) => this.startResize(e, resizer));
        });
    }

    startResize(e, resizer) {
        e.preventDefault();
        this.isResizing = true;
        this.currentResizer = resizer;
        this.startX = e.clientX;

        // Store initial widths
        const columns = Array.from(this.container.children);
        this.startWidths = columns.map(col => col.offsetWidth);

        // Add visual feedback
        document.body.classList.add('resizing');
        
        // Bind events
        document.addEventListener('mousemove', this.handleMouseMove.bind(this));
        document.addEventListener('mouseup', this.stopResize.bind(this));
    }

    handleMouseMove(e) {
        if (!this.isResizing || !this.currentResizer) return;

        const deltaX = e.clientX - this.startX;
        const columns = Array.from(this.container.children);
        const resizers = Array.from(this.container.querySelectorAll('.resizer'));
        const resizerIndex = resizers.indexOf(this.currentResizer);
        
        const leftColumn = columns[resizerIndex];
        const rightColumn = columns[resizerIndex + 1];
        
        if (!leftColumn || !rightColumn) return;

        const containerWidth = this.container.offsetWidth;
        const newLeftWidth = this.startWidths[resizerIndex] + deltaX;
        const newRightWidth = this.startWidths[resizerIndex + 1] - deltaX;

        // Smart limits based on column position
        const limits = this.getResizeLimits(resizerIndex, containerWidth);
        
        // Check limits
        if (newLeftWidth < limits.minLeft || newLeftWidth > limits.maxLeft) return;
        if (newRightWidth < limits.minRight || newRightWidth > limits.maxRight) return;

        // Apply new widths
        leftColumn.style.width = newLeftWidth + 'px';
        rightColumn.style.width = newRightWidth + 'px';
    }

    getResizeLimits(resizerIndex, containerWidth) {
        const minWidth = 250;
        
        if (resizerIndex === 0) {
            // Left edge: left column vs middle column
            return {
                minLeft: minWidth,
                maxLeft: containerWidth * 0.4, // Max 40% of screen
                minRight: minWidth,
                maxRight: containerWidth * 0.8  // Middle can be max 80%
            };
        } else {
            // Right edge: middle column vs right column  
            return {
                minLeft: minWidth,
                maxLeft: containerWidth * 0.7, // Middle can be max 70%
                minRight: minWidth,
                maxRight: containerWidth * 0.45 // Right max 45% of screen
            };
        }
    }

    stopResize() {
        if (!this.isResizing) return;

        this.isResizing = false;
        this.currentResizer = null;
        document.body.classList.remove('resizing');
        
        // Remove event listeners
        document.removeEventListener('mousemove', this.handleMouseMove.bind(this));
        document.removeEventListener('mouseup', this.stopResize.bind(this));
    }
}

// ===== CHAT INTERFACE MODULE =====
class ChatInterface {
    constructor(elements) {
        this.elements = elements;
        this.messageCount = 0;
        
        this.init();
    }

    init() {
        // Auto-expanding textarea
        this.elements.messageInput.addEventListener('input', () => this.autoResize());
        
        // Send message handlers
        this.elements.messageInput.addEventListener('keydown', (e) => this.handleKeydown(e));
        this.elements.sendButton.addEventListener('click', () => this.sendMessage());

        // Initial setup
        this.autoResize();
    }

    autoResize() {
        const input = this.elements.messageInput;
        
        // Reset height to calculate scroll height
        input.style.height = 'auto';
        
        const scrollHeight = input.scrollHeight;
        const maxHeight = 120; // Max height (about 6 lines)
        const minHeight = 20;  // Min height (1 line)
        
        // Set new height within limits
        const newHeight = Math.min(Math.max(scrollHeight, minHeight), maxHeight);
        input.style.height = newHeight + 'px';
        
        // Enable/disable scrolling based on content
        if (scrollHeight > maxHeight) {
            input.style.overflowY = 'auto';
        } else {
            input.style.overflowY = 'hidden';
        }
    }

    handleKeydown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            this.sendMessage();
        }
        
        // Adjust height after key events
        setTimeout(() => this.autoResize(), 0);
    }

    sendMessage() {
        const text = this.elements.messageInput.value.trim();
        if (!text) return;

        // Disable send button temporarily
        this.toggleSendButton(false);

        // Add user message
        this.addMessage(text, 'user');

        // Clear input and reset height
        this.elements.messageInput.value = '';
        this.autoResize();

        // Simulate AI response (replace with actual backend call)
        this.simulateAIResponse(text);
    }

    addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        messageDiv.setAttribute('data-message-type', type);
        messageDiv.setAttribute('data-message-id', ++this.messageCount);

        const icon = type === 'user' ? 'fas fa-user' : 'fas fa-robot';
        
        messageDiv.innerHTML = `
            <i class="${icon}"></i>
            <span class="message-content">${this.escapeHtml(content)}</span>
        `;

        this.elements.messagesArea.appendChild(messageDiv);
        this.scrollToBottom();

        return messageDiv;
    }

    simulateAIResponse(userMessage) {
        // Add loading indicator
        const loadingMsg = this.addMessage('Thinking...', 'ai');
        
        // Simulate API delay
        setTimeout(() => {
            // Remove loading message
            loadingMsg.remove();
            
            // Add actual response
            const response = `I received your message: "${userMessage}". How can I help you with your lesson planning?`;
            this.addMessage(response, 'ai');
            
            // Re-enable send button
            this.toggleSendButton(true);
        }, 800);
    }

    // BACKEND INTEGRATION READY - Replace simulateAIResponse with this
    async sendToBackend(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    model: 'gpt-4' // Get from model indicator
                })
            });

            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error('Error sending message to backend:', error);
            return 'Sorry, there was an error processing your message.';
        }
    }

    toggleSendButton(enabled) {
        this.elements.sendButton.disabled = !enabled;
        this.elements.sendButton.style.opacity = enabled ? '1' : '0.6';
    }

    scrollToBottom() {
        const messagesArea = this.elements.messagesArea;
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    adjustLayout() {
        // Called when window resizes or layout changes
        this.autoResize();
    }
}

// ===== FILE UPLOADER MODULE =====
class FileUploader {
    constructor(elements) {
        this.elements = elements;
        this.uploadedFile = null;
        
        this.init();
    }

    init() {
        this.elements.button.addEventListener('click', () => this.handleUpload());
    }

    handleUpload() {
        // Create file input
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.pdf,.doc,.docx,.txt,.ppt,.pptx';
        
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.processFile(file);
            }
        });

        fileInput.click();
    }

    processFile(file) {
        this.uploadedFile = file;
        
        // Update UI
        this.updateUploadButton('Processing...');
        
        // Display file info in middle column
        this.displayFileInfo(file);
        
        // Simulate file processing (replace with actual backend call)
        this.simulateFileProcessing(file);
    }

    // BACKEND INTEGRATION READY
    async uploadToBackend(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error uploading file:', error);
            throw error;
        }
    }

    simulateFileProcessing(file) {
        setTimeout(() => {
            this.updateUploadButton('Upload File');
            console.log('File processed:', file.name);
        }, 1500);
    }

    displayFileInfo(file) {
        const displayArea = this.elements.displayArea;
        
        displayArea.innerHTML = `
            <div style="text-align: center; padding: 20px;">
                <i class="fas fa-file-check" style="font-size: 3rem; color: #4C50CC; margin-bottom: 16px;"></i>
                <h3 style="margin: 0 0 8px 0; color: #374151;">${file.name}</h3>
                <p style="margin: 0; color: #6b7280;">Size: ${this.formatFileSize(file.size)}</p>
                <p style="margin: 8px 0 0 0; color: #6b7280;">Type: ${file.type || 'Unknown'}</p>
            </div>
        `;
    }

    updateUploadButton(text) {
        const button = this.elements.button;
        const icon = button.querySelector('i');
        const isProcessing = text === 'Processing...';
        
        button.innerHTML = `
            <i class="fas fa-${isProcessing ? 'spinner fa-spin' : 'upload'}"></i>
            ${text}
        `;
        
        button.disabled = isProcessing;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// ===== UTILITY FUNCTIONS =====
const Utils = {
    // Debounce function for performance
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Format timestamp
    formatTime(date = new Date()) {
        return date.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    },

    // Show notification (for future use)
    showNotification(message, type = 'info') {
        console.log(`[${type.toUpperCase()}] ${message}`);
        // TODO: Implement actual notification system
    }
};

// ===== BACKEND API HELPERS =====
const API = {
    // Base configuration
    baseURL: '/api',
    
    // Generic API call helper
    async call(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Chat endpoints
    chat: {
        send: async (message, model = 'gpt-4') => {
            return await API.call('/chat', {
                method: 'POST',
                body: JSON.stringify({ message, model })
            });
        }
    },

    // File endpoints
    files: {
        upload: async (file) => {
            const formData = new FormData();
            formData.append('file', file);
            
            return await fetch(`${API.baseURL}/upload`, {
                method: 'POST',
                body: formData
            }).then(res => res.json());
        },
        
        analyze: async (fileId) => {
            return await API.call(`/files/${fileId}/analyze`);
        }
    }
};

// ===== APP STARTUP =====
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the main application
    window.easyLessonApp = new EasyLessonApp();
    
    // Global error handler
    window.addEventListener('error', (e) => {
        console.error('Application Error:', e.error);
        Utils.showNotification('An error occurred. Please refresh the page.', 'error');
    });
    
    console.log('EasyLesson loaded successfully!');
});