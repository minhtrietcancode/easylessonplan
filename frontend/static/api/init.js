/**
 * API Initialization Entry Point
 * Single file to initialize all APIs and expose them globally
 */
import { apiManager } from './core/APIManager.js';

class APIInitializer {
    constructor() {
        this.initPromise = null;
    }

    /**
     * Initialize all APIs once
     */
    async initialize() {
        if (this.initPromise) {
            return this.initPromise;
        }

        this.initPromise = this._doInitialization();
        return this.initPromise;
    }

    async _doInitialization() {
        try {
            console.log('Initializing APIs...');
            
            // Wait a tick to ensure routes.js has loaded
            await new Promise(resolve => setTimeout(resolve, 0));
            
            // Initialize API manager
            await apiManager.initialize();

            // Expose to window for global access
            this._exposeToWindow();

            console.log('All APIs initialized and exposed to window');
            
            // Dispatch ready event
            window.dispatchEvent(new CustomEvent('apisReady'));
            
            return true;
        } catch (error) {
            console.error('API initialization failed:', error);
            window.dispatchEvent(new CustomEvent('apisError', { detail: error }));
            throw error;
        }
    }

    _exposeToWindow() {
        // Clean, organized window exposure
        window.API = {
            auth: apiManager.getAPI('auth'),
            llm: apiManager.getAPI('llm'),
            manager: apiManager
        };

        // Legacy support (if needed)
        window.authAPI = apiManager.getAPI('auth');
        window.llmAPI = apiManager.getAPI('llm');
    }
}

// Create and initialize
const apiInitializer = new APIInitializer();

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        apiInitializer.initialize();
    });
} else {
    apiInitializer.initialize();
}

// Export for manual initialization if needed
export { apiInitializer };