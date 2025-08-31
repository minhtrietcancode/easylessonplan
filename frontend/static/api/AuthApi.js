/**
 * Authentication API Client
 * Handles user authentication, session management, and user info
 */

class AuthApi {
    constructor(apiClient = window.ApiClient) {
        this.client = apiClient;
        this.endpoints = {
            user: '/auth/user',
            logout: '/auth/logout',
            validate: '/auth/session/validate'
        };
    }

    /**
     * Get current user information
     */
    async getCurrentUser() {
        try {
            const response = await this.client.get(this.endpoints.user);
            return {
                user: response.user,
                authenticated: response.authenticated,
                success: true
            };
        } catch (error) {
            console.warn('Failed to get user info:', error.message);
            return {
                user: null,
                authenticated: false,
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Logout current user
     */
    async logout() {
        try {
            const response = await this.client.post(this.endpoints.logout);
            return {
                success: true,
                message: response.message
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Validate current session
     */
    async validateSession() {
        try {
            const response = await this.client.get(this.endpoints.validate);
            return {
                valid: response.valid,
                user: response.user,
                success: true
            };
        } catch (error) {
            return {
                valid: false,
                user: null,
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Check if user is authenticated
     */
    async isAuthenticated() {
        const userData = await this.getCurrentUser();
        return userData.authenticated;
    }

    /**
     * Get user's first name
     */
    getFirstName(fullName) {
        return fullName ? fullName.split(' ')[0] : 'User';
    }
}

// Export singleton instance
window.AuthApi = window.AuthApi || new AuthApi();