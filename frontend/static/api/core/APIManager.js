/**
 * Centralized API Manager
 * Handles initialization and provides clean access to all APIs
 */
import { APIClient } from './APIClient.js';
import { APIError } from './APIError.js';

export class APIManager {
    constructor() {
        this.client = new APIClient();
        this.isInitialized = false;
    }

    /**
     * Initialize all API modules
     */
    async initialize() {
        if (this.isInitialized) return;

        try {
            // Ensure routes are available
            if (!window.API_ROUTES) {
                throw new Error('API_ROUTES not loaded. Ensure routes.js is loaded first.');
            }

            // Initialize API modules
            this.auth = await this._initAuthAPI();
            this.llm = await this._initLLMAPI();

            this.isInitialized = true;
            console.log('✅ API Manager initialized successfully');
        } catch (error) {
            console.error('❌ API Manager initialization failed:', error);
            throw error;
        }
    }

    async _initAuthAPI() {
        const { AuthAPI } = await import('../service/auth_api.js');
        return new AuthAPI(this.client);
    }

    async _initLLMAPI() {
        const { LLMAPI } = await import('../service/llm_api.js');
        return new LLMAPI(this.client);
    }

    /**
     * Get API instance (ensures initialization)
     */
    getAPI(apiName) {
        if (!this.isInitialized) {
            throw new Error('APIManager not initialized. Call initialize() first.');
        }
        return this[apiName];
    }
}

// Create singleton
export const apiManager = new APIManager();