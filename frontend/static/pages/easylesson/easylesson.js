// File: frontend/static/pages/easylesson/easylesson.js
// ===== EASYLESSON APP - FLASK INTEGRATED =====

// ===== APP INITIALIZATION =====
class EasyLessonApp {
    constructor() {
        this.elements = this.initializeElements();
        this.resizer = new ColumnResizer(this.elements.container);
        this.chatInterface = new ChatInterface(this.elements.chat);
        this.modelSelector = new ModelSelector(this.elements.modelSelector);
        
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
            modelSelector: {
                indicator: document.getElementById('modelIndicator'),
                modelName: document.getElementById('modelName')
            }
        };
    }

    async init() {
        console.log('EasyLesson App Initializing...');
        
        // Wait for APIs to be ready
        if (!window.API) {
            await new Promise((resolve) => {
                if (window.API) {
                    resolve();
                } else {
                    window.addEventListener('apisReady', resolve, { once: true });
                }
            });
        }
        
        // Load available models
        await this.modelSelector.loadAvailableModels();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            this.chatInterface.adjustLayout();
        });
        
        console.log('EasyLesson App Initialized');
    }
}

// ===== MODEL SELECTOR MODULE - UPDATED FOR DROP-UP =====
class ModelSelector {
    constructor(elements) {
        this.elements = elements;
        this.availableModels = [];
        this.currentModel = '';
        this.isDropdownOpen = false;
        
        this.init();
    }

    init() {
        // Make model indicator clickable
        this.elements.indicator.style.cursor = 'pointer';
        this.elements.indicator.addEventListener('click', () => this.toggleDropdown());
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.elements.indicator.contains(e.target)) {
                this.closeDropdown();
            }
        });
    }

    async loadAvailableModels() {
        try {
            console.log('📡 Fetching available models...');
            // Use local mock data (no backend integration)
            const response = await window.llmAPI.getAvailableModels();

            if (response.success) {
                this.availableModels = response.data.models || [];
                this.currentModel = response.data.current_model || 'Default';
            } else {
                console.error('❌ Backend error loading models:', response.message);
                this.availableModels = ['Default']; // Fallback
                this.currentModel = 'Default'; // Fallback
                Utils.showNotification(response.message || 'Failed to load models from backend', 'error');
            }
            
            // Update UI
            this.elements.modelName.textContent = this.currentModel;
            
            console.log('✅ Models loaded:', this.availableModels);
            console.log('✅ Current model:', this.currentModel);
        } catch (error) {
            console.error('❌ Error loading models:', error);
            // Set default values
            this.availableModels = ['Default'];
            this.currentModel = 'Default';
            this.elements.modelName.textContent = 'Default';
            Utils.showNotification('Failed to load available models due to network error', 'error');
        }
    }

    toggleDropdown() {
        if (this.isDropdownOpen) {
            this.closeDropdown();
        } else {
            this.openDropdown();
        }
    }

    openDropdown() {
        this.isDropdownOpen = true;
        
        // Create dropdown element
        const dropdown = document.createElement('div');
        dropdown.className = 'model-dropdown drop-up';
        
        // Calculate dropdown height to position it properly
        const estimatedHeight = Math.min(this.availableModels.length * 45 + 10, 200); // 45px per item + padding, max 200px
        
        dropdown.style.cssText = `
            position: absolute;
            bottom: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            margin-bottom: 4px;
            max-height: 200px;
            overflow-y: auto;
            animation: dropUpSlideIn 0.2s ease;
        `;

        // Add model options (reverse order so current selection appears at bottom)
        const modelsToShow = [...this.availableModels].reverse();
        modelsToShow.forEach(modelName => {
            const option = document.createElement('div');
            option.className = 'model-option';
            option.style.cssText = `
                padding: 10px 12px;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: background-color 0.2s ease;
                border-bottom: 1px solid #f1f5f9;
                ${modelName === this.currentModel ? 'background-color: #f1f5f9; font-weight: 600;' : ''}
            `;
            
            // Remove border from last item (which is actually first due to reverse)
            if (modelName === modelsToShow[modelsToShow.length - 1]) {
                option.style.borderBottom = 'none';
            }
            
            option.innerHTML = `
                <i class="fas fa-brain" style="color: #4C50CC;"></i>
                <span>${modelName}</span>
                ${modelName === this.currentModel ? '<i class="fas fa-check" style="color: #10b981; margin-left: auto;"></i>' : ''}
            `;
            
            option.addEventListener('mouseenter', () => {
                if (modelName !== this.currentModel) {
                    option.style.backgroundColor = '#f8fafc';
                }
            });
            
            option.addEventListener('mouseleave', () => {
                if (modelName !== this.currentModel) {
                    option.style.backgroundColor = 'transparent';
                }
            });
            
            option.addEventListener('click', () => this.selectModel(modelName));
            
            dropdown.appendChild(option);
        });

        // Position dropdown relative to indicator
        this.elements.indicator.style.position = 'relative';
        this.elements.indicator.appendChild(dropdown);
        
        // Scroll to current model if it exists in the dropdown
        setTimeout(() => {
            const currentOption = dropdown.querySelector('.model-option[style*="font-weight: 600"]');
            if (currentOption) {
                currentOption.scrollIntoView({ block: 'nearest' });
            }
        }, 50);
    }

    closeDropdown() {
        this.isDropdownOpen = false;
        const dropdown = this.elements.indicator.querySelector('.model-dropdown');
        if (dropdown) {
            // Add slide out animation
            dropdown.style.animation = 'dropUpSlideOut 0.2s ease';
            setTimeout(() => dropdown.remove(), 200);
        }
    }

    async selectModel(modelName) {
        if (modelName === this.currentModel) {
            this.closeDropdown();
            return;
        }

        try {
            // Show loading state
            const originalText = this.elements.modelName.textContent;
            this.elements.modelName.textContent = 'Switching...';
            this.elements.indicator.style.opacity = '0.6';
            
            console.log('🔄 Switching to model:', modelName);
            const response = await window.llmAPI.switchModel(modelName);

            if (response.success) {
                this.currentModel = modelName;
                this.elements.modelName.textContent = this.currentModel;
                this.elements.indicator.style.opacity = '1';
                
                // Close dropdown
                this.closeDropdown();
                
                // Show success message
                Utils.showNotification(`Switched to ${modelName}`, 'success');
                console.log('✅ Model switched successfully:', this.currentModel);
            } else {
                console.error('❌ Backend error switching model:', response.message);
                this.elements.modelName.textContent = originalText; // Revert on error
                this.elements.indicator.style.opacity = '1';
                Utils.showNotification(response.message || 'Failed to switch model', 'error');
            }
            
        } catch (error) {
            console.error('❌ Error switching model:', error);
            this.elements.modelName.textContent = this.currentModel;
            this.elements.indicator.style.opacity = '1';
            Utils.showNotification('Failed to switch model due to network error', 'error');
        }
    }
}

// ===== CHAT INTERFACE MODULE =====
class ChatInterface {
    constructor(elements) {
        this.elements = elements;
        this.messageCount = 0;
        this.isWaitingForResponse = false;
        
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

    async sendMessage() {
        const text = this.elements.messageInput.value.trim();
        if (!text || this.isWaitingForResponse) return;

        // Disable send button temporarily
        this.toggleSendButton(false);
        this.isWaitingForResponse = true;

        // Add user message
        this.addMessage(text, 'user');

        // Clear input and reset height
        this.elements.messageInput.value = '';
        this.autoResize();

        // Add loading message
        const loadingMsg = this.addMessage('Thinking...', 'ai', true);

        try {
            // Mocked AI reply (no backend)
            // await new Promise(res => setTimeout(res, 600));
            const response = await window.llmAPI.sendMessageToLLM(text);

            // Remove loading message
            loadingMsg.remove();

            if (response.success) {
                // Display the actual LLM response
                this.addMessage(response.data.reply, 'ai');
            } else {
                console.error('❌ Backend error getting LLM response:', response.message);
                this.addMessage(response.message || 'Error: Failed to get response from AI.', 'ai');
                Utils.showNotification(response.message || 'Failed to get LLM response', 'error');
            }

        } finally {
            // Re-enable send button
            this.toggleSendButton(true);
            this.isWaitingForResponse = false;
        }
    }

    addMessage(content, type, isLoading = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message ${isLoading ? 'loading-message' : ''}`;
        messageDiv.setAttribute('data-message-type', type);
        messageDiv.setAttribute('data-message-id', ++this.messageCount);

        const icon = type === 'user' ? 'fas fa-user' : 'fas fa-robot';
        
        messageDiv.innerHTML = `
            <i class="${icon} ${isLoading ? 'fa-spin' : ''}"></i>
            <span class="message-content">${this.escapeHtml(content)}</span>
        `;

        this.elements.messagesArea.appendChild(messageDiv);
        this.scrollToBottom();

        return messageDiv;
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

    // Show notification
    showNotification(message, type = 'info') {
        console.log(`[${type.toUpperCase()}] ${message}`);
        
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 16px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 9999;
            animation: slideInRight 0.3s ease;
            ${type === 'success' ? 'background-color: #10b981;' : ''}
            ${type === 'error' ? 'background-color: #ef4444;' : ''}
            ${type === 'info' ? 'background-color: #3b82f6;' : ''}
        `;
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
};


// ===== APP STARTUP =====
document.addEventListener('DOMContentLoaded', () => {
    // Add notification styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(100px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes slideOutRight {
            from {
                opacity: 1;
                transform: translateX(0);
            }
            to {
                opacity: 0;
                transform: translateX(100px);
            }
        }
        
        .loading-message {
            opacity: 0.8;
        }
        
        .loading-message .fa-robot {
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    `;
    document.head.appendChild(style);
    
    // Initialize the main application
    window.easyLessonApp = new EasyLessonApp();
    
    // Global error handler
    window.addEventListener('error', (e) => {
        console.error('Application Error:', e.error);
        Utils.showNotification('An error occurred. Please refresh the page.', 'error');
    });
    
    console.log('EasyLesson loaded successfully!');
});