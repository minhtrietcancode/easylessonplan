"""
EasyLesson Lesson Planning API Module
Handles all lesson planning and LLM-related functionality
"""

from flask import Blueprint, jsonify, request
from .base_api import BaseAPI
from ..llm.LlmManager import LlmManager
from ..llm.LlmConfig import LlmConfig

lesson_bp = Blueprint('lesson', __name__, url_prefix='/api/lesson')

class LessonAPI(BaseAPI):
    """API class for lesson planning functionality"""
    
    def __init__(self):
        super().__init__()
        self.llm_service = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize LLM service"""
        try:
            self.llm_service = LlmManager()
        except Exception as e:
            print(f"❌ Failed to initialize LLM Service: {e}")
            self.llm_service = None
    
    def chat(self):
        """Handle chat messages"""
        try:
            if not self.llm_service or not self.llm_service.is_available():
                return self.error_response('LLM Service not initialized', 500)
            
            data = request.get_json()
            if not data or 'message' not in data:
                return self.error_response('No message provided', 400)
            
            message = data['message'].strip()
            response = self.llm_service.send_message(message)
            
            return self.success_response({
                'response': response,
                'model': self.llm_service.get_current_model()
            })
        except Exception as e:
            return self.error_response(f'Chat processing failed: {str(e)}', 500)
    
    def get_available_models(self):
        """Get list of available LLM models"""
        try:
            if not self.llm_service or not self.llm_service.is_available():
                return self.error_response('LLM Service not initialized', 500)
            
            return self.success_response({
                'models': self.llm_service.get_available_models(),
                'current_model': self.llm_service.get_current_model()
            })
        except Exception as e:
            return self.error_response(f'Failed to get available models: {str(e)}', 500)
    
    def switch_model(self):
        """Switch to a different LLM model"""
        try:
            if not self.llm_service or not self.llm_service.is_available():
                return self.error_response('LLM Service not initialized', 500)
            
            data = request.get_json()
            if not data or 'model_name' not in data:
                return self.error_response('No model name provided', 400)
            
            model_name = data['model_name']
            switched_model = self.llm_service.switch_model(model_name)
            
            return self.success_response({
                'current_model': switched_model,
                'message': f'Successfully switched to {switched_model}'
            })
        except Exception as e:
            return self.error_response(f'Failed to switch model: {str(e)}', 500)
    
    def clear_conversation(self):
        """Clear conversation history"""
        try:
            if not self.llm_service or not self.llm_service.is_available():
                return self.error_response('LLM Service not initialized', 500)
            
            self.llm_service.clear_conversation()
            return self.success_response({'message': 'Conversation cleared'})
        except Exception as e:
            return self.error_response(f'Failed to clear conversation: {str(e)}', 500)
    
    def get_conversation_history(self):
        """Get current conversation history"""
        try:
            if not self.llm_service or not self.llm_service.is_available():
                return self.error_response('LLM Service not initialized', 500)
            
            history_data = self.llm_service.get_conversation_history()
            return self.success_response(history_data)
        except Exception as e:
            return self.error_response(f'Failed to get conversation history: {str(e)}', 500)


# Create API instance
lesson_api = LessonAPI()

# Register routes
lesson_bp.add_url_rule('/chat', 'chat', lesson_api.chat, methods=['POST'])
lesson_bp.add_url_rule('/models', 'models', lesson_api.get_available_models, methods=['GET'])
lesson_bp.add_url_rule('/models/switch', 'switch_model', lesson_api.switch_model, methods=['POST'])
lesson_bp.add_url_rule('/conversation/clear', 'clear_conversation', lesson_api.clear_conversation, methods=['POST'])
lesson_bp.add_url_rule('/conversation/history', 'conversation_history', lesson_api.get_conversation_history, methods=['GET'])
