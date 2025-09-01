/**
 * API Module Index
 * Coordinates all API modules and provides a unified interface
 */

class APIManager {
    /**
     * Centralized API management
     */
    
    constructor() {
        this.initialized = false;
        this.modules = {};
    }
    
    /**
     * Initialize all API modules
     * @returns {Promise<boolean>} - Success status
     */
    async initialize() {
        try {
            console.log('🔗 Initializing API modules...');
            
            // Check if all required modules are loaded
            if (!window.APIClient || !window.AuthAPI || !window.UserAPI || !window.LessonAPI) {
                throw new Error('Required API modules not loaded');
            }
            
            // Initialize modules
            this.modules = {
                client: window.apiClient,
                auth: window.authAPI,
                user: window.userAPI,
                lesson: window.lessonAPI,
                authState: window.authStateManager,
                userPreferences: window.userPreferencesManager,
                userData: window.userDataManager
            };
            
            // Initialize auth state manager
            if (this.modules.authState) {
                await this.modules.authState.initialize();
            }
            
            this.initialized = true;
            console.log('✅ API modules initialized successfully');
            
            return true;
            
        } catch (error) {
            console.error('❌ API initialization failed:', error);
            this.initialized = false;
            return false;
        }
    }
    
    /**
     * Get API module by name
     * @param {string} moduleName - Name of the module
     * @returns {object|null} - API module or null
     */
    getModule(moduleName) {
        if (!this.initialized) {
            console.warn('API manager not initialized');
            return null;
        }
        
        return this.modules[moduleName] || null;
    }
    
    /**
     * Check if API manager is ready
     * @returns {boolean} - Ready status
     */
    isReady() {
        return this.initialized;
    }
    
    /**
     * Get all available modules
     * @returns {object} - Object with all modules
     */
    getAllModules() {
        return this.initialized ? { ...this.modules } : {};
    }
    
    /**
     * Refresh all modules (useful for auth state changes)
     * @returns {Promise<void>}
     */
    async refresh() {
        if (this.modules.authState) {
            await this.modules.authState.refresh();
        }
        
        if (this.modules.userData) {
            this.modules.userData.clearCache();
        }
    }
}


/**
 * Global API utilities
 */
class APIUtils {
    /**
     * Utility functions for API operations
     */
    
    /**
     * Handle API response with loading state
     * @param {Promise} apiCall - API call promise
     * @param {string} loadingElement - Selector for loading element
     * @returns {Promise<object>} - API response
     */
    static async handleWithLoading(apiCall, loadingElement = null) {
        let loadingEl = null;
        
        if (loadingElement) {
            loadingEl = document.querySelector(loadingElement);
            if (loadingEl) {
                loadingEl.style.display = 'block';
            }
        }
        
        try {
            const response = await apiCall;
            return response;
        } finally {
            if (loadingEl) {
                loadingEl.style.display = 'none';
            }
        }
    }
    
    /**
     * Debounce API calls
     * @param {function} func - Function to debounce
     * @param {number} delay - Delay in milliseconds
     * @returns {function} - Debounced function
     */
    static debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }
    
    /**
     * Retry API call with exponential backoff
     * @param {function} apiCall - API call function
     * @param {number} maxRetries - Maximum number of retries
     * @param {number} baseDelay - Base delay in milliseconds
     * @returns {Promise<object>} - API response
     */
    static async retryWithBackoff(apiCall, maxRetries = 3, baseDelay = 1000) {
        let lastError;
        
        for (let attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                return await apiCall();
            } catch (error) {
                lastError = error;
                
                if (attempt === maxRetries) {
                    break;
                }
                
                // Calculate delay with exponential backoff
                const delay = baseDelay * Math.pow(2, attempt);
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
        
        throw lastError;
    }
    
    /**
     * Format API error for display
     * @param {APIError} error - API error object
     * @returns {string} - Formatted error message
     */
    static formatError(error) {
        if (!error) return 'Unknown error occurred';
        
        if (error.status === 0) {
            return 'Network connection issue';
        } else if (error.status === 401) {
            return 'Authentication required';
        } else if (error.status === 403) {
            return 'Access denied';
        } else if (error.status === 404) {
            return 'Resource not found';
        } else if (error.status >= 500) {
            return 'Server error. Please try again later';
        }
        
        return error.message || `Error ${error.status}`;
    }
}


// Create singleton API manager
const apiManager = new APIManager();

// Auto-initialize when all modules are loaded
document.addEventListener('DOMContentLoaded', async () => {
    // Wait a bit for all scripts to load
    setTimeout(async () => {
        await apiManager.initialize();
    }, 100);
});

// Export for global use
window.APIManager = APIManager;
window.APIUtils = APIUtils;
window.apiManager = apiManager;