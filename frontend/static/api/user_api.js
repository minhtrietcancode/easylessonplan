/**
 * User API Module
 * Handles user-related API calls and operations
 */

class UserAPI {
    /**
     * User API client for profile and user data operations
     */
    
    constructor() {
        this.client = new window.APIClient();
    }
    
    /**
     * Get user profile information
     * @returns {Promise<object>} - User profile response
     */
    async getProfile() {
        return await this.client.get(window.API_ROUTES.USER.GET_PROFILE);
    }
    
    /**
     * Update user profile
     * @param {object} profileData - Profile data to update
     * @returns {Promise<object>} - Update response
     */
    async updateProfile(profileData) {
        return await this.client.put(window.API_ROUTES.USER.PUT_UPDATE_PROFILE, profileData);
    }
    
    /**
     * Get dashboard data for user
     * @returns {Promise<object>} - Dashboard data response
     */
    async getDashboardData() {
        return await this.client.get(window.API_ROUTES.USER.GET_DASHBOARD_DATA);
    }
    
    /**
     * Get user activity log
     * @param {number} limit - Maximum number of activities to fetch
     * @returns {Promise<object>} - Activity log response
     */
    async getActivityLog(limit = 10) {
        return await this.client.get(window.API_ROUTES.USER.GET_ACTIVITY_LOG, { limit });
    }
    
    /**
     * Get user statistics
     * @returns {Promise<object>} - User statistics response
     */
    async getStatistics() {
        return await this.client.get(window.API_ROUTES.USER.GET_STATISTICS);
    }
    
    /**
     * Handle user-related errors
     * @param {APIError} error - API error object
     */
    handleUserError(error) {
        const userMessages = {
            'PROFILE_NOT_FOUND': 'Profile information not found',
            'INVALID_FIELDS': 'Some profile fields are invalid',
            'UPDATE_FAILED': 'Failed to update profile. Please try again'
        };
        
        const message = userMessages[error.errorCode] || error.message || 'User operation failed';
        window.ResponseHandler.showErrorMessage({ message });
    }
}


/**
 * User data manager for client-side user state
 */
class UserDataManager {
    /**
     * Manages user data and local state
     */
    
    constructor() {
        this.userAPI = new UserAPI();
        this.userData = null;
        this.lastUpdated = null;
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }
    
    /**
     * Get user data with caching
     * @param {boolean} forceRefresh - Force refresh from server
     * @returns {Promise<object>} - User data
     */
    async getUserData(forceRefresh = false) {
        const now = Date.now();
        
        // Return cached data if fresh and not forcing refresh
        if (!forceRefresh && this.userData && this.lastUpdated && 
            (now - this.lastUpdated) < this.cacheTimeout) {
            return this.userData;
        }
        
        try {
            const response = await this.userAPI.getProfile();
            
            if (response.success) {
                this.userData = response.data;
                this.lastUpdated = now;
                return this.userData;
            } else {
                throw new Error(response.message);
            }
            
        } catch (error) {
            console.error('Failed to get user data:', error);
            // Return cached data if available, otherwise null
            return this.userData;
        }
    }
    
    /**
     * Update user data both locally and on server
     * @param {object} updates - Data to update
     * @returns {Promise<object>} - Updated user data
     */
    async updateUserData(updates) {
        try {
            const response = await this.userAPI.updateProfile(updates);
            
            if (response.success) {
                // Update local cache
                this.userData = { ...this.userData, ...response.data };
                this.lastUpdated = Date.now();
                
                window.ResponseHandler.showSuccessMessage('Profile updated successfully');
                return this.userData;
            } else {
                throw new Error(response.message);
            }
            
        } catch (error) {
            this.userAPI.handleUserError(error);
            throw error;
        }
    }
    
    /**
     * Clear cached user data
     */
    clearCache() {
        this.userData = null;
        this.lastUpdated = null;
    }
    
    /**
     * Get specific user field
     * @param {string} field - Field name
     * @param {any} defaultValue - Default value if field not found
     * @returns {any} - Field value
     */
    getUserField(field, defaultValue = null) {
        return this.userData?.[field] ?? defaultValue;
    }
    
    /**
     * Check if user data is loaded
     * @returns {boolean} - True if user data is available
     */
    isLoaded() {
        return this.userData !== null;
    }
}


/**
 * User preferences manager
 */
class UserPreferencesManager {
    /**
     * Manages user preferences with local storage fallback
     */
    
    constructor() {
        this.authAPI = new window.AuthAPI();
        this.preferences = {};
        this.defaultPreferences = {
            theme: 'light',
            language: 'en',
            notifications: true,
            auto_save: true
        };
    }
    
    /**
     * Load user preferences
     * @returns {Promise<object>} - User preferences
     */
    async loadPreferences() {
        try {
            const response = await this.authAPI.getUserPreferences();
            
            if (response.success) {
                this.preferences = { ...this.defaultPreferences, ...response.data };
            } else {
                this.preferences = { ...this.defaultPreferences };
            }
            
            return this.preferences;
            
        } catch (error) {
            console.warn('Failed to load preferences:', error);
            this.preferences = { ...this.defaultPreferences };
            return this.preferences;
        }
    }
    
    /**
     * Update user preferences
     * @param {object} updates - Preference updates
     * @returns {Promise<boolean>} - Success status
     */
    async updatePreferences(updates) {
        try {
            const response = await this.authAPI.updateUserPreferences(updates);
            
            if (response.success) {
                this.preferences = { ...this.preferences, ...updates };
                this.applyPreferences();
                return true;
            }
            
            return false;
            
        } catch (error) {
            window.authAPI.handleAuthError(error);
            return false;
        }
    }
    
    /**
     * Get preference value
     * @param {string} key - Preference key
     * @param {any} defaultValue - Default value
     * @returns {any} - Preference value
     */
    getPreference(key, defaultValue = null) {
        return this.preferences[key] ?? this.defaultPreferences[key] ?? defaultValue;
    }
    
    /**
     * Apply preferences to UI
     */
    applyPreferences() {
        // Apply theme
        const theme = this.getPreference('theme');
        document.documentElement.setAttribute('data-theme', theme);
        
        // Apply other preferences as needed
        // This can be expanded based on what preferences affect
    }
    
    /**
     * Reset preferences to defaults
     * @returns {Promise<boolean>} - Success status
     */
    async resetToDefaults() {
        return await this.updatePreferences(this.defaultPreferences);
    }
}


// Create singleton instances
const userAPI = new UserAPI();
const userDataManager = new UserDataManager();
const userPreferencesManager = new UserPreferencesManager();

// Export for global use
window.UserAPI = UserAPI;
window.UserDataManager = UserDataManager;
window.UserPreferencesManager = UserPreferencesManager;
window.userAPI = userAPI; // Export the instance
window.userDataManager = userDataManager; // Export the instance
window.userPreferencesManager = userPreferencesManager; // Export the instance