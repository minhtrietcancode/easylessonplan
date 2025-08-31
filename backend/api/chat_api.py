"""
Chat API Routes
Handles chat messaging, conversation management, and LLM interactions
"""

from flask import Blueprint, request, jsonify
from .auth_api import api_login_required

chat_api_bp = Blueprint('chat_api', __name__)

# This will be injected by the main app
llm_service = None

def set_llm_service(service):
    """Set the LLM service instance"""
    global llm_service
    llm_service = service

@chat_api_bp.route('/send', methods=['POST'])
@api_login_required
def send_message():
    """Send a message to the LLM and get response"""
    try:
        if not llm_service or not llm_service.is_available():
            return jsonify({'error': 'LLM Service not available'}), 503
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        message = data.get('message', '').strip()
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Process message
        response = llm_service.send_message(message)
        
        return jsonify({
            'response': response,
            'model': llm_service.get_current_model(),
            'status': 'success'
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Chat processing failed: {str(e)}'}), 500

@chat_api_bp.route('/history', methods=['GET'])
@api_login_required
def get_conversation_history():
    """Get current conversation history"""
    try:
        if not llm_service:
            return jsonify({'error': 'LLM Service not available'}), 503
        
        history_data = llm_service.get_conversation_history()
        return jsonify({
            **history_data,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get conversation history: {str(e)}'}), 500

@chat_api_bp.route('/clear', methods=['POST'])
@api_login_required
def clear_conversation():
    """Clear conversation history"""
    try:
        if not llm_service:
            return jsonify({'error': 'LLM Service not available'}), 503
        
        llm_service.clear_conversation()
        return jsonify({
            'status': 'success',
            'message': 'Conversation cleared'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to clear conversation: {str(e)}'}), 500