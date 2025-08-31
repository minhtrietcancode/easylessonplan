/**
 * API Module Exports
 * Central entry point for all API clients
 */

// Ensure all API clients are loaded
if (typeof window.ApiClient === 'undefined') {
    console.error('ApiClient not loaded! Make sure to include ApiClient.js first');
}

// Create API factory object
window.API = {
    // Core client
    client: window.ApiClient,
    
    // Domain-specific APIs
    auth: window.AuthApi,
    chat: window.ChatApi,
    models: window.ModelApi,
    
    // Utility methods
    utils: {
        /**
         * Check if all APIs are available
         */
        validateAPIs() {
            const apis = ['ApiClient', 'AuthApi', 'ChatApi', 'ModelApi'];
            const missing = apis.filter(api => typeof window[api] === 'undefined');
            
            if (missing.length > 0) {
                console.warn('Missing API clients:', missing);
                return false;
            }
            
            return true;
        },

        /**
         * Initialize all API clients with custom config
         */
        initialize(config = {}) {
            const baseURL = config.baseURL || '/api/v1';
            
            // Reinitialize with custom config if needed
            if (config.baseURL) {
                window.ApiClient = new ApiClient(baseURL);
                window.AuthApi = new AuthApi(window.ApiClient);
                window.ChatApi = new ChatApi(window.ApiClient);
                window.ModelApi = new ModelApi(window.ApiClient);
                
                // Update API references
                this.client = window.ApiClient;
                this.auth = window.AuthApi;
                this.chat = window.ChatApi;
                this.models = window.ModelApi;
            }
            
            console.log('API clients initialized with base URL:', baseURL);
        }
    }
};

// Validate that all APIs loaded correctly
document.addEventListener('DOMContentLoaded', () => {
    if (window.API.utils.validateAPIs()) {
        console.log('✅ All API clients loaded successfully');
    } else {
        console.error('❌ Some API clients failed to load');
    }
});

// Export for potential module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = window.API;
}