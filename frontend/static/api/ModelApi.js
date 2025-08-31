/**
 * Model Management API Client
 * Handles LLM model listing, switching, and status
 */

class ModelApi {
    constructor(apiClient = window.ApiClient) {
        this.client = apiClient;
        this.endpoints = {
            available: '/models/available',
            switch: '/models/switch',
            current: '/models/current'
        };
    }

    /**
     * Get available models
     */
    async getAvailableModels() {
        try {
            const response = await this.client.get(this.endpoints.available);
            return {
                models: response.models || [],
                currentModel: response.current_model,
                count: response.count || 0,
                success: true
            };
        } catch (error) {
            return {
                models: [],
                currentModel: null,
                count: 0,
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Switch to a different model
     */
    async switchModel(modelName) {
        if (!modelName || typeof modelName !== 'string') {
            throw new Error('Model name is required');
        }

        try {
            const response = await this.client.post(this.endpoints.switch, {
                model_name: modelName
            });

            return {
                currentModel: response.current_model,
                message: response.message,
                success: true
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Get current active model
     */
    async getCurrentModel() {
        try {
            const response = await this.client.get(this.endpoints.current);
            return {
                currentModel: response.current_model,
                success: true
            };
        } catch (error) {
            return {
                currentModel: null,
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Validate if a model name exists in available models
     */
    async validateModel(modelName) {
        const { models, success } = await this.getAvailableModels();
        
        if (!success) {
            return { valid: false, error: 'Could not fetch available models' };
        }
        
        return {
            valid: models.includes(modelName),
            error: models.includes(modelName) ? null : `Model "${modelName}" not available`
        };
    }
}

// Export singleton instance
window.ModelApi = window.ModelApi || new ModelApi();