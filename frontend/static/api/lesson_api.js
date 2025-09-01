/**
 * Lesson Planning API Client
 * Handles communication with lesson planning endpoints
 */

class LessonAPI {
    constructor(client) {
        this.client = client;
        this.baseEndpoint = '/api/lesson';
        console.log('🔧 LessonAPI initialized with base endpoint:', this.baseEndpoint);
        
        // Test the connection
        this.testConnection();
    }

    /**
     * Test the API connection
     * @private
     */
    async testConnection() {
        try {
            await this.getAvailableModels();
            console.log('✅ LessonAPI connection test successful');
        } catch (error) {
            console.error('❌ LessonAPI connection test failed:', error);
        }
    }

    /**
     * Send a chat message to the LLM
     * @param {string} message - User's message
     * @returns {Promise<object>} - API response with LLM reply
     */
    async sendMessage(message) {
        console.log('🚀 Sending chat message:', message);
        try {
            const response = await this.client.post(`${this.baseEndpoint}/chat`, { message });
            console.log('✅ Chat response:', response);
            return response;
        } catch (error) {
            console.error('❌ Chat error:', error);
            throw error;
        }
    }

    /**
     * Get available LLM models
     * @returns {Promise<object>} - List of available models and current model
     */
    async getAvailableModels() {
        console.log('🔍 Getting available models...');
        try {
            const response = await this.client.get(`${this.baseEndpoint}/models`);
            console.log('✅ Models response:', response);
            return response;
        } catch (error) {
            console.error('❌ Models error:', error);
            throw error;
        }
    }

    /**
     * Switch to a different LLM model
     * @param {string} modelName - Name of the model to switch to
     * @returns {Promise<object>} - Response with new model info
     */
    async switchModel(modelName) {
        console.log('🔄 Switching to model:', modelName);
        try {
            const response = await this.client.post(`${this.baseEndpoint}/models/switch`, { model_name: modelName });
            console.log('✅ Switch response:', response);
            return response;
        } catch (error) {
            console.error('❌ Switch error:', error);
            throw error;
        }
    }

    /**
     * Clear conversation history
     * @returns {Promise<object>} - Success response
     */
    async clearConversation() {
        return this.client.post(`${this.baseEndpoint}/conversation/clear`);
    }

    /**
     * Get conversation history
     * @returns {Promise<object>} - Chat history data
     */
    async getConversationHistory() {
        return this.client.get(`${this.baseEndpoint}/conversation/history`);
    }
}

// Export to window object
window.LessonAPI = LessonAPI;
