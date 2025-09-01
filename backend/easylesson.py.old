from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys

# Add the backend directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your LLM modules
from llm.LlmManager import LlmManager
from llm.LlmConfig import LlmConfig


# ===== CONFIGURATION CLASS =====
class AppConfig:
    """Centralized application configuration"""
    
    def __init__(self):
        self.debug = self._get_bool_env('FLASK_DEBUG', True)
        self.port = self._get_int_env('FLASK_PORT', 5000)
        self.host = os.getenv('FLASK_HOST', '127.0.0.1')
    
    def _get_bool_env(self, key, default):
        """Get boolean environment variable"""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def _get_int_env(self, key, default):
        """Get integer environment variable"""
        try:
            return int(os.getenv(key, default))
        except (ValueError, TypeError):
            return default


# ===== LLM SERVICE CLASS =====
class LlmService:
    """Handles all LLM-related operations and conversation management"""
    
    def __init__(self):
        self.llm_manager = None
        self.conversation_history = []
        self._initialize_manager()
    
    def _initialize_manager(self):
        """Initialize the LLM Manager"""
        try:
            self.llm_manager = LlmManager()
            print(f"✅ LLM Manager initialized with models: {self.get_available_models()}")
        except Exception as e:
            print(f"❌ Failed to initialize LLM Manager: {e}")
            self.llm_manager = None
    
    def is_available(self):
        """Check if LLM service is available"""
        return self.llm_manager is not None
    
    def get_available_models(self):
        """Get list of available models"""
        if not self.is_available():
            return []
        return self.llm_manager.get_available_models()
    
    def get_current_model(self):
        """Get current active model"""
        if not self.is_available():
            return None
        return self.llm_manager.getCurrentModelName()
    
    def switch_model(self, model_name):
        """Switch to a different model"""
        if not self.is_available():
            raise Exception("LLM Manager not initialized")
        
        if not model_name:
            raise ValueError("Model name is required")
        
        self.llm_manager.setCurrentModel(model_name)
        return model_name
    
    def send_message(self, message):
        """Process a chat message and return response"""
        if not self.is_available():
            raise Exception("LLM Manager not initialized")
        
        if not message or not message.strip():
            raise ValueError("Message is required")
        
        # Add user message to history
        self._add_to_history('user', message)
        
        # Build context and get response
        context_message = self._build_context_message()
        response = self.llm_manager.invoke(context_message)
        
        # Add AI response to history
        self._add_to_history('assistant', response)
        
        return response
    
    def _add_to_history(self, role, content):
        """Add message to conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'model': self.get_current_model()
        })
    
    def _build_context_message(self):
        """Build context message from conversation history"""
        if not self.conversation_history:
            return ""
        
        # Use last 20 messages to avoid token limits
        recent_history = self.conversation_history[-20:]
        
        context_parts = []
        for msg in recent_history:
            if msg['role'] == 'user':
                context_parts.append(f"User: {msg['content']}")
            else:
                context_parts.append(f"Assistant: {msg['content']}")
        
        # Get the latest user message
        latest_user_msg = self.conversation_history[-1]['content']
        
        # Build full message with context
        if len(context_parts) > 1:
            context = "\n".join(context_parts[:-1])
            return f"Previous conversation context:\n{context}\n\nCurrent question: {latest_user_msg}"
        else:
            return latest_user_msg
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_history(self):
        """Get current conversation history"""
        return {
            'history': self.conversation_history,
            'count': len(self.conversation_history)
        }


# ===== API HELPERS CLASS =====
class ApiHelpers:
    """Utility methods for API handling"""
    
    @staticmethod
    def validate_json_request(request):
        """Validate and return JSON data from request"""
        if not request.is_json:
            raise ValueError('Request must be JSON')
        
        data = request.get_json()
        if data is None:
            raise ValueError('Invalid JSON data')
        
        return data
    
    @staticmethod
    def handle_api_error(error, default_message="An error occurred"):
        """Standardized API error handling"""
        error_message = str(error) if str(error) else default_message
        print(f"API Error: {error_message}")
        return jsonify({'error': error_message}), 500


# ===== MAIN APPLICATION CLASS =====
class EasyLessonApp:
    """Main Flask application with all routes and services"""
    
    def __init__(self):
        self.config = AppConfig()
        self.app = self._create_app()
        self.llm_service = None
        self._initialize_services()
        self._register_routes()
        self._register_error_handlers()
    
    def _create_app(self):
        """Create and configure Flask app"""
        app = Flask(__name__, 
                   template_folder='../frontend/templates',
                   static_folder='../frontend/static')
        CORS(app)
        return app
    
    def _initialize_services(self):
        """Initialize all application services"""
        try:
            self.llm_service = LlmService()
        except Exception as e:
            print(f"❌ Failed to initialize LLM Service: {e}")
            self.llm_service = None
    
    def _register_routes(self):
        """Register all application routes"""
        
        # ===== WEB ROUTES =====
        @self.app.route('/')
        def index():
            """Serve the main application page"""
            return render_template('easylesson.html')
        
        # ===== API ROUTES =====
        @self.app.route('/api/models', methods=['GET'])
        def get_available_models():
            """Get list of available LLM models"""
            try:
                if not self.llm_service or not self.llm_service.is_available():
                    return jsonify({'error': 'LLM Service not initialized'}), 500
                
                models = self.llm_service.get_available_models()
                current_model = self.llm_service.get_current_model()
                
                return jsonify({
                    'models': models,
                    'current_model': current_model,
                    'status': 'success'
                })
            except Exception as e:
                return ApiHelpers.handle_api_error(e, 'Failed to get available models')

        @self.app.route('/api/models/switch', methods=['POST'])
        def switch_model():
            """Switch to a different LLM model"""
            try:
                data = ApiHelpers.validate_json_request(request)
                model_name = data.get('model_name')
                
                if not self.llm_service or not self.llm_service.is_available():
                    return jsonify({'error': 'LLM Service not initialized'}), 500
                
                # Switch the model
                switched_model = self.llm_service.switch_model(model_name)
                
                return jsonify({
                    'status': 'success',
                    'current_model': switched_model,
                    'message': f'Successfully switched to {switched_model}'
                })
                
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            except Exception as e:
                return ApiHelpers.handle_api_error(e, 'Failed to switch model')

        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            """Handle chat messages"""
            try:
                data = ApiHelpers.validate_json_request(request)
                message = data.get('message', '').strip()
                
                if not self.llm_service or not self.llm_service.is_available():
                    return jsonify({'error': 'LLM Service not initialized'}), 500
                
                # Process message and get response
                response = self.llm_service.send_message(message)
                
                return jsonify({
                    'response': response,
                    'model': self.llm_service.get_current_model(),
                    'status': 'success'
                })
                
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
            except Exception as e:
                return ApiHelpers.handle_api_error(e, 'Chat processing failed')

        @self.app.route('/api/conversation/clear', methods=['POST'])
        def clear_conversation():
            """Clear conversation history"""
            try:
                if not self.llm_service:
                    return jsonify({'error': 'LLM Service not initialized'}), 500
                
                self.llm_service.clear_conversation()
                return jsonify({'status': 'success', 'message': 'Conversation cleared'})
                
            except Exception as e:
                return ApiHelpers.handle_api_error(e, 'Failed to clear conversation')

        @self.app.route('/api/conversation/history', methods=['GET'])
        def get_conversation_history():
            """Get current conversation history"""
            try:
                if not self.llm_service:
                    return jsonify({'error': 'LLM Service not initialized'}), 500
                
                history_data = self.llm_service.get_conversation_history()
                return jsonify({
                    **history_data,
                    'status': 'success'
                })
                
            except Exception as e:
                return ApiHelpers.handle_api_error(e, 'Failed to get conversation history')

        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'llm_service_status': 'initialized' if self.llm_service and self.llm_service.is_available() else 'not initialized',
                'available_models': self.llm_service.get_available_models() if self.llm_service and self.llm_service.is_available() else [],
                'current_model': self.llm_service.get_current_model() if self.llm_service and self.llm_service.is_available() else None
            })
    
    def _register_error_handlers(self):
        """Register global error handlers"""
        
        @self.app.errorhandler(404)
        def not_found(e):
            return jsonify({'error': 'Endpoint not found'}), 404

        @self.app.errorhandler(500)
        def internal_error(e):
            return jsonify({'error': 'Internal server error'}), 500

        @self.app.errorhandler(400)
        def bad_request(e):
            return jsonify({'error': 'Bad request'}), 400
    
    def run(self):
        """Run the Flask application"""
        print(f"🚀 Starting EasyLesson Flask Server...")
        print(f"📍 URL: http://{self.config.host}:{self.config.port}")
        print(f"🔧 Debug Mode: {self.config.debug}")
        
        if self.llm_service and self.llm_service.is_available():
            print(f"🤖 Available Models: {self.llm_service.get_available_models()}")
            print(f"✨ Current Model: {self.llm_service.get_current_model()}")
        else:
            print("⚠️  Warning: LLM Service not initialized")
        
        self.app.run(
            host=self.config.host, 
            port=self.config.port, 
            debug=self.config.debug
        )


# ===== APPLICATION ENTRY POINT =====
if __name__ == '__main__':
    # Create and run the application
    easy_lesson_app = EasyLessonApp()
    easy_lesson_app.run()