/**
 * Authentication API Service
 * Clean, dependency-free auth API
 */
export class AuthAPI {
    constructor(client) {
        this.client = client;
    }
    
    /**
     * Get current user information
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
     */
    initiateLogin() {
        window.location.href = window.API_ROUTES.GET_LOGIN;
    }
}