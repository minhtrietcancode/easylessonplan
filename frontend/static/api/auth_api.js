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

/**
 * Authentication state manager
 */
class AuthStateManager {
    constructor() {
        this.authAPI = new AuthAPI();
        this.currentUser = null;
        this.isAuthenticated = false;
        this.listeners = [];
    }
    
    /**
     * Add listener for auth state changes
     * @param {function} callback - Callback function
     */
    addAuthStateListener(callback) {
        this.listeners.push(callback);
    }
    
    /**
     * Notify all listeners of auth state change
     */
    notifyListeners() {
        this.listeners.forEach(callback => {
            try {
                callback({
                    user: this.currentUser,
                    authenticated: this.isAuthenticated
                });
            } catch (error) {
                console.error('Auth state listener error:', error);
            }
        });
    }
    
    /**
     * Initialize authentication state
     * @returns {Promise<object>} - Auth state
     */
    async initialize() {
        try {
            const response = await this.authAPI.getUserInfo();
            
            if (response.success && response.data) {
                this.currentUser = response.data.user;
                this.isAuthenticated = response.data.authenticated;
            } else {
                this.currentUser = null;
                this.isAuthenticated = false;
            }
            
            this.notifyListeners();
            return { user: this.currentUser, authenticated: this.isAuthenticated };
            
        } catch (error) {
            console.error('Auth initialization failed:', error);
            this.currentUser = null;
            this.isAuthenticated = false;
            this.notifyListeners();
            return { user: null, authenticated: false };
        }
    }
    
    /**
     * Refresh authentication state
     * @returns {Promise<void>}
     */
    async refresh() {
        await this.initialize();
    }
}

// Create singleton instances
const authAPI = new AuthAPI();
const authStateManager = new AuthStateManager();

// Export for global use
window.AuthAPI = AuthAPI;
window.AuthStateManager = AuthStateManager;
window.authAPI = authAPI;
window.authStateManager = authStateManager;