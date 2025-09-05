// File: frontend/static/api/api_client.js
/**
 * API Client Module
 * Centralized HTTP client for all API communication
 */

class APIClient {
    constructor() {
        this.defaultHeaders = {
            'Content-Type': 'application/json'
        };
    }
    
    /**
     * Generic request method
     * @param {string} endpoint - API endpoint
     * @param {object} options - Request options
     * @returns {Promise<object>} - API response
     */
    async request(endpoint, options = {}) {
        const url = endpoint;
        
        const config = {
            headers: { ...this.defaultHeaders, ...options.headers },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            
            const contentType = response.headers.get('content-type');
            let data;
            
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                data = await response.text();
            }
            
            if (!response.ok) {
                throw new APIError(
                    data.message || `HTTP ${response.status}`,
                    response.status,
                    data.error_code,
                    data
                );
            }
            
            return data;
            
        } catch (error) {
            if (error instanceof APIError) {
                throw error;
            }
            
            throw new APIError(
                'Network error or server unavailable',
                0,
                'NETWORK_ERROR',
                { originalError: error.message }
            );
        }
    }
    
    /**
     * GET request
     * @param {string} endpoint - API endpoint
     * @param {object} params - Query parameters
     * @returns {Promise<object>} - API response
     */
    async get(endpoint, params = {}) {
        const urlParams = new URLSearchParams(params);
        const queryString = urlParams.toString();
        const fullEndpoint = queryString ? `${endpoint}?${queryString}` : endpoint;
        
        return this.request(fullEndpoint, { method: 'GET' });
    }
    
    /**
     * POST request
     * @param {string} endpoint - API endpoint
     * @param {object} data - Request body data
     * @returns {Promise<object>} - API response
     */
    async post(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    /**
     * PUT request
     * @param {string} endpoint - API endpoint
     * @param {object} data - Request body data
     * @returns {Promise<object>} - API response
     */
    async put(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
}

/**
 * Custom API Error class
 */
class APIError extends Error {
    constructor(message, status, errorCode, details) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.errorCode = errorCode;
        this.details = details;
    }
}

// Create singleton instance
const apiClient = new APIClient();

// Export for use in other modules
window.APIClient = APIClient;
window.APIError = APIError;
window.apiClient = apiClient;