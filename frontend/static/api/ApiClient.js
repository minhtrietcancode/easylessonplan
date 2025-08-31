/**
 * Base API Client
 * Provides common HTTP client functionality with error handling, retries, and configuration
 */

class ApiClient {
    constructor(baseURL = '/api/v1') {
        this.baseURL = baseURL;
        this.defaultHeaders = {
            'Content-Type': 'application/json'
        };
        this.timeout = 30000; // 30 seconds
    }

    /**
     * Generic API call method
     */
    async call(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                ...this.defaultHeaders,
                ...options.headers
            },
            ...options
        };

        // Add timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        config.signal = controller.signal;

        try {
            const response = await fetch(url, config);
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                await this.handleHttpError(response);
            }
            
            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            this.handleNetworkError(error);
            throw error;
        }
    }

    /**
     * Handle HTTP errors (4xx, 5xx)
     */
    async handleHttpError(response) {
        let errorMessage = `HTTP ${response.status}`;
        
        try {
            const errorData = await response.json();
            errorMessage = errorData.error || errorMessage;
        } catch {
            // Fallback if response is not JSON
            errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        }
        
        throw new Error(errorMessage);
    }

    /**
     * Handle network errors (timeouts, connection issues)
     */
    handleNetworkError(error) {
        if (error.name === 'AbortError') {
            console.error('Request timeout');
        } else {
            console.error('Network error:', error.message);
        }
    }

    /**
     * HTTP method helpers
     */
    async get(endpoint, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = queryString ? `${endpoint}?${queryString}` : endpoint;
        
        return this.call(url, { method: 'GET' });
    }

    async post(endpoint, data = {}) {
        return this.call(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async put(endpoint, data = {}) {
        return this.call(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async delete(endpoint) {
        return this.call(endpoint, { method: 'DELETE' });
    }
}

// Export singleton instance
window.ApiClient = window.ApiClient || new ApiClient();