/**
 * API Client Module
 * Centralized HTTP client for all API communication
 */

class APIClient {
    /**
     * Base API client with common functionality
     */
    
    constructor(baseURL = '') {
        this.baseURL = baseURL;
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
        const url = `${this.baseURL}${endpoint}`;
        
        const config = {
            headers: { ...this.defaultHeaders, ...options.headers },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            
            // Handle different content types
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
            
            // Network or other errors
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
    
    /**
     * DELETE request
     * @param {string} endpoint - API endpoint
     * @returns {Promise<object>} - API response
     */
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
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
    
    toString() {
        return `APIError (${this.status}): ${this.message}`;
    }
}


/**
 * Response handler utility
 */
class ResponseHandler {
    /**
     * Handle API response with success/error callbacks
     * @param {Promise} apiCall - API call promise
     * @param {function} onSuccess - Success callback
     * @param {function} onError - Error callback
     */
    static async handle(apiCall, onSuccess, onError) {
        try {
            const response = await apiCall;
            if (onSuccess) {
                onSuccess(response);
            }
            return response;
        } catch (error) {
            console.error('API Error:', error);
            if (onError) {
                onError(error);
            }
            throw error;
        }
    }
    
    /**
     * Show user-friendly error message
     * @param {APIError} error - API error object
     */
    static showErrorMessage(error) {
        // Create a simple toast notification
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ef4444;
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            max-width: 300px;
        `;
        
        toast.textContent = error.message || 'An error occurred';
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }
    
    /**
     * Show success message
     * @param {string} message - Success message
     */
    static showSuccessMessage(message) {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            max-width: 300px;
        `;
        
        toast.textContent = message;
        document.body.appendChild(toast);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }
}


// Create singleton instance
const apiClient = new APIClient('/api');

// Export for use in other modules
window.APIClient = APIClient;
window.APIError = APIError;
window.ResponseHandler = ResponseHandler;
window.apiClient = apiClient;