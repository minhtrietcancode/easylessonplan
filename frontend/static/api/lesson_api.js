/**
 * Lesson Planning API Client
 * Handles communication with lesson planning endpoints
 */

class LessonAPI {
    constructor(client) {
        this.client = client;
        this.baseEndpoint = '/api/lesson';
    }

    /**
     * Send a chat message to the LLM
     * @param {string} message - User's message
     * @returns {Promise<object>} - API response with LLM reply
     */
    async sendMessage(message) {
        return this.client.post(`${this.baseEndpoint}/chat`, { message });
    }

    /**
     * Get available LLM models
     * @returns {Promise<object>} - List of available models and current model
     */
    async getAvailableModels() {
        return this.client.get(`${this.baseEndpoint}/models`);
    }

    /**
     * Switch to a different LLM model
     * @param {string} modelName - Name of the model to switch to
     * @returns {Promise<object>} - Response with new model info
     */
    async switchModel(modelName) {
        return this.client.post(`${this.baseEndpoint}/models/switch`, { model_name: modelName });
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

// Export for use in index.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { LessonAPI };
}
