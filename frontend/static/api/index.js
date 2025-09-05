// File: frontend/static/api/index.js
/**
 * API Module Index
 * Coordinates all API modules and provides a unified interface
 */

class APIManager {
    constructor() {
        this.initialized = false;
    }
    
    /**
     * Initialize all API modules
     * @returns {Promise<boolean>} - Success status
     */
    async initialize() {
        try {
            console.log('Initializing API modules...');
            
            // Check if all required modules are loaded
            if (!window.APIClient || !window.AuthAPI) {
                throw new Error('Required API modules not loaded');
            }
            
            // Initialize auth state manager
            if (window.authStateManager) {
                await window.authStateManager.initialize();
            }
            
            this.initialized = true;
            console.log('API modules initialized successfully');
            
            return true;
            
        } catch (error) {
            console.error('API initialization failed:', error);
            this.initialized = false;
            return false;
        }
    }
    
    /**
     * Check if API manager is ready
     * @returns {boolean} - Ready status
     */
    isReady() {
        return this.initialized;
    }
}

// Create singleton API manager
const apiManager = new APIManager();

// Auto-initialize when all modules are loaded
document.addEventListener('DOMContentLoaded', async () => {
    setTimeout(async () => {
        await apiManager.initialize();
    }, 100);
});

// Export for global use
window.APIManager = APIManager;
window.apiManager = apiManager;