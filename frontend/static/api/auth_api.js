/**
 * Authentication API Module
 * Handles all authentication-related API calls
 */

class AuthAPI {
    /**
     * Authentication API client
     */
    
    constructor() {
        this.client = new window.APIClient();
    }
    
    /**
     * Check current authentication status
     * @returns {Promise<object>} - Auth status response
     */
    async checkAuthStatus() {
        try {
            return await this.client.get('/api/auth/status');
        } catch (error) {
            console.warn('Auth status check failed:', error.message);
            return { 
                success: false, 
                data: { authenticated: false, user: null },
                message: 'Auth check failed'
            };
        }
    }
    
    /**
     * Get current user information
     * @returns {Promise<object>} - User info response
     */
    async getUserInfo() {
        try {
            return await this.client.get('/api/auth/user');
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
     * Validate current session
     * @returns {Promise<object>} - Session validation response
     */
    async validateSession() {
        return await this.client.get('/api/auth/validate');
    }
    
    /**
     * Get user preferences
     * @returns {Promise<object>} - User preferences response
     */
    async getUserPreferences() {
        return await this.client.get('/api/auth/preferences');
    }
    
    /**
     * Update user preferences
     * @param {object} preferences - Preferences to update
     * @returns {Promise<object>} - Update response
     */
    async updateUserPreferences(preferences) {
        return await this.client.put('/api/auth/preferences', preferences);
    }
    
    /**
     * Initiate login process
     * @returns {void} - Redirects to OAuth flow
     */
    initiateLogin() {
        window.location.href = '/auth/login';
    }
    
    /**
     * Logout user
     * @returns {void} - Redirects to home page
     */
    logout() {
        window.location.href = '/auth/logout';
    }
    
    /**
     * Handle authentication errors with user-friendly messages
     * @param {APIError} error - API error object
     */
    handleAuthError(error) {
        const userMessages = {
            'AUTH_REQUIRED': 'Please log in to continue',
            'INVALID_SESSION': 'Your session has expired. Please log in again',
            'NETWORK_ERROR': 'Connection issue. Please check your internet and try again'
        };
        
        const message = userMessages[error.errorCode] || error.message || 'Authentication error occurred';
        window.ResponseHandler.showErrorMessage({ message });
        
        // If auth error, might need to redirect to login
        if (error.status === 401) {
            setTimeout(() => {
                this.initiateLogin();
            }, 2000);
        }
    }
}


/**
 * Authentication state manager
 */
class AuthStateManager {
    /**
     * Manages authentication state and UI updates
     */
    
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
     * Remove auth state listener
     * @param {function} callback - Callback function to remove
     */
    removeAuthStateListener(callback) {
        this.listeners = this.listeners.filter(listener => listener !== callback);
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
    
    /**
     * Get current authentication state
     * @returns {object} - Current auth state
     */
    getState() {
        return {
            user: this.currentUser,
            authenticated: this.isAuthenticated
        };
    }
    
    /**
     * Check if user has specific permission
     * @param {string} permission - Permission to check
     * @returns {boolean} - True if user has permission
     */
    hasPermission(permission) {
        // Placeholder for permission checking
        // Can be expanded based on user roles/permissions
        return this.isAuthenticated;
    }
}


// Create singleton instances
const authAPI = new AuthAPI();
const authStateManager = new AuthStateManager();

// Export for global use
window.AuthAPI = AuthAPI;
window.AuthStateManager = AuthStateManager;
window.authAPI = authAPI; // Export the instance
window.authStateManager = authStateManager; // Export the instance