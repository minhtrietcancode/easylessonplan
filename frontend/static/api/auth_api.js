// File: frontend/static/api/auth_api.js
/**
 * Authentication API Module
 * Handles all authentication-related API calls
 */

class AuthAPI {
    constructor() {
        this.client = new window.APIClient();
    }
    
    /**
     * Get current user information
     * @returns {Promise<object>} - User info response
     */
    async getUserInfo() {
        try {
            return await this.client.get(window.API_ROUTES.AUTH.GET_USER_INFO);
        } catch (error) {
            console.warn('User info fetch failed:', error.message);
            return { 
                success: false, 
                data: { user: null, authenticated: false },
                message: 'Failed to get user info'
            };
        }
    }
    
    /**
     * Initiate login process
     * @returns {void} - Redirects to OAuth flow
     */
    initiateLogin() {
        window.location.href = window.OAUTH_ROUTES.GET_LOGIN;
    }
}

// Create singleton instance
const authAPI = new AuthAPI();

// Export for global use
window.AuthAPI = AuthAPI;
window.authAPI = authAPI;