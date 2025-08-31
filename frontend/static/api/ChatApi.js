/**
 * Chat API Client
 * Handles chat messaging, conversation management, and LLM interactions
 */

class ChatApi {
    constructor(apiClient = window.ApiClient) {
        this.client = apiClient;
        this.endpoints = {
            send: '/chat/send',
            history: '/chat/history',
            clear: '/chat/clear'
        };
    }

    /**
     * Send a message to the LLM
     */
    async sendMessage(message) {
        if (!message || !message.trim()) {
            throw new Error('Message cannot be empty');
        }

        try {
            const response = await this.client.post(this.endpoints.send, {
                message: message.trim()
            });

            return {
                response: response.response,
                model: response.model,
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
     * Get conversation history
     */
    async getHistory() {
        try {
            const response = await this.client.get(this.endpoints.history);
            return {
                history: response.history || [],
                count: response.count || 0,
                success: true
            };
        } catch (error) {
            return {
                history: [],
                count: 0,
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Clear conversation history
     */
    async clearConversation() {
        try {
            const response = await this.client.post(this.endpoints.clear);
            return {
                success: true,
                message: response.message
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Validate message before sending
     */
    validateMessage(message) {
        if (!message || typeof message !== 'string') {
            return { valid: false, error: 'Message must be a non-empty string' };
        }
        
        const trimmed = message.trim();
        if (!trimmed) {
            return { valid: false, error: 'Message cannot be empty' };
        }
        
        if (trimmed.length > 4000) {
            return { valid: false, error: 'Message too long (max 4000 characters)' };
        }
        
        return { valid: true, message: trimmed };
    }
}

// Export singleton instance
window.ChatApi = window.ChatApi || new ChatApi();