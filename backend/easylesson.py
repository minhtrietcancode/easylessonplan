from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys

# Add the backend directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your LLM modules
from llm.LlmManager import LlmManager
from llm.LlmConfig import LlmConfig

app = Flask(__name__, 
           template_folder='../frontend/templates',
           static_folder='../frontend/static')
CORS(app)

# Global variables for managing state
llm_manager = None
conversation_history = []  # Store conversation context across model changes

def init_llm_manager():
    """Initialize the LLM Manager"""
    global llm_manager
    try:
        llm_manager = LlmManager()
        print(f"✅ LLM Manager initialized with models: {llm_manager.get_available_models()}")
    except Exception as e:
        print(f"❌ Failed to initialize LLM Manager: {e}")
        llm_manager = None

# ===== ROUTES =====

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('easylesson.html')

@app.route('/api/models', methods=['GET'])
def get_available_models():
    """Get list of available LLM models"""
    try:
        if llm_manager is None:
            return jsonify({'error': 'LLM Manager not initialized'}), 500
            
        models = llm_manager.get_available_models()
        current_model = llm_manager.getCurrentModelName()
        
        return jsonify({
            'models': models,
            'current_model': current_model,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/switch', methods=['POST'])
def switch_model():
    """Switch to a different LLM model"""
    try:
        data = request.get_json()
        model_name = data.get('model_name')
        
        if not model_name:
            return jsonify({'error': 'model_name is required'}), 400
            
        if llm_manager is None:
            return jsonify({'error': 'LLM Manager not initialized'}), 500
            
        # Switch the model
        llm_manager.setCurrentModel(model_name)
        
        return jsonify({
            'status': 'success',
            'current_model': model_name,
            'message': f'Successfully switched to {model_name}'
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to switch model: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
            
        if llm_manager is None:
            return jsonify({'error': 'LLM Manager not initialized'}), 500
        
        # Add user message to conversation history
        conversation_history.append({
            'role': 'user',
            'content': message,
            'model': llm_manager.getCurrentModelName()
        })
        
        # Build context from conversation history
        context_message = build_context_message()
        
        # Get response from current model
        response = llm_manager.invoke(context_message)
        
        # Add AI response to conversation history
        conversation_history.append({
            'role': 'assistant', 
            'content': response,
            'model': llm_manager.getCurrentModelName()
        })
        
        return jsonify({
            'response': response,
            'model': llm_manager.getCurrentModelName(),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Chat error: {str(e)}'}), 500

def build_context_message():
    """Build context message from conversation history"""
    if not conversation_history:
        return ""
    
    # Build context from recent conversation (last 10 exchanges to avoid token limits)
    recent_history = conversation_history[-20:]  # Last 20 messages (10 exchanges)
    
    context_parts = []
    for msg in recent_history:
        if msg['role'] == 'user':
            context_parts.append(f"User: {msg['content']}")
        else:
            context_parts.append(f"Assistant: {msg['content']}")
    
    # Get the latest user message
    latest_user_msg = conversation_history[-1]['content'] if conversation_history else ""
    
    # If we have context, include it
    if len(context_parts) > 1:
        context = "\n".join(context_parts[:-1])  # All except the latest message
        full_message = f"Previous conversation context:\n{context}\n\nCurrent question: {latest_user_msg}"
    else:
        full_message = latest_user_msg
    
    return full_message

@app.route('/api/conversation/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'success', 'message': 'Conversation cleared'})

@app.route('/api/conversation/history', methods=['GET'])
def get_conversation_history():
    """Get current conversation history"""
    return jsonify({
        'history': conversation_history,
        'count': len(conversation_history),
        'status': 'success'
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'llm_manager_status': 'initialized' if llm_manager else 'not initialized',
        'available_models': llm_manager.get_available_models() if llm_manager else [],
        'current_model': llm_manager.getCurrentModelName() if llm_manager else None
    })

# ===== ERROR HANDLERS =====

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# ===== APP STARTUP =====

def create_app():
    """Application factory"""
    # Initialize LLM Manager
    init_llm_manager()
    
    return app

if __name__ == '__main__':
    # Create the app
    app = create_app()
    
    # Development settings
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    
    print(f"🚀 Starting EasyLesson Flask Server...")
    print(f"📍 URL: http://{host}:{port}")
    print(f"🔧 Debug Mode: {debug_mode}")
    
    if llm_manager:
        print(f"🤖 Available Models: {llm_manager.get_available_models()}")
        print(f"✨ Current Model: {llm_manager.getCurrentModelName()}")
    else:
        print("⚠️  Warning: LLM Manager not initialized")
    
    app.run(host=host, port=port, debug=debug_mode)