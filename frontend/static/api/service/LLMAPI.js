/**
 * LLM API Service
 * Clean, dependency-free LLM API
 */
export class LLMAPI {
    constructor(client) {
        this.client = client;
    }

    /**
     * Fetches available LLM models and current active model
     */
    async getAvailableModels() {
        return await this.client.get(window.API_ROUTES.LLM.GET_MODELS_LIST);
    }

    /**
     * Sets the current active LLM model
     */
    async switchModel(modelName) {
        return await this.client.put(window.API_ROUTES.LLM.PUT_SWITCH_MODEL, { model_name: modelName });
    }

    /**
     * Sends a message to the currently active LLM
     */
    async sendMessageToLLM(message) {
        return await this.client.post(window.API_ROUTES.LLM.POST_SEND_MESSAGE, { message: message });
    }
}