// File: frontend/static/api/user_api.js
/**
 * User API Module
 * Handles user-related API calls and operations
 */

class UserAPI {
    constructor() {
        this.client = new window.APIClient();
    }
}

// Create singleton instance
const userAPI = new UserAPI();

// Export for global use
window.UserAPI = UserAPI;
window.userAPI = userAPI;