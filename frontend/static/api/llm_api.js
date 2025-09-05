window.llmAPI = {
    /**
     * Fetches the list of available LLM models and the current active model.
     * @returns {Promise<Object>} A promise that resolves to an object containing models and current_model.
     */
    getAvailableModels: async function() {
        return await new window.APIClient().get('/api/llm/models');
    },

    /**
     * Sets the current active LLM model.
     * @param {string} modelName The name of the model to set as current.
     * @returns {Promise<Object>} A promise that resolves to the API response.
     */
    switchModel: async function(modelName) {
        return await new window.APIClient().put('/api/llm/models', { model_name: modelName });
    },

    /**
     * Sends a message to the currently active LLM and retrieves its response.
     * @param {string} message The message to send to the LLM.
     * @returns {Promise<Object>} A promise that resolves to an object containing the LLM's reply.
     */
    sendMessageToLLM: async function(message) {
        return await new window.APIClient().post('/api/llm/chat', { message: message });
    }
};
