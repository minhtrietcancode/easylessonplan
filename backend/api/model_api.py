"""
Model Management API Routes
Handles LLM model listing, switching, and configuration
"""

from flask import Blueprint, request, jsonify
from .auth_api import api_login_required

model_api_bp = Blueprint('model_api', __name__)

# This will be injected by the main app
llm_service = None

def set_llm_service(service):
    """Set the LLM service instance"""
    global llm_service
    llm_service = service

@model_api_bp.route('/available', methods=['GET'])
@api_login_required
def get_available_models():
    """Get list of available LLM models"""
    try:
        if not llm_service or not llm_service.is_available():
            return jsonify({'error': 'LLM Service not available'}), 503
        
        models = llm_service.get_available_models()
        current_model = llm_service.get_current_model()
        
        return jsonify({
            'models': models,
            'current_model': current_model,
            'count': len(models),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get available models: {str(e)}'}), 500

@model_api_bp.route('/switch', methods=['POST'])
@api_login_required
def switch_model():
    """Switch to a different LLM model"""
    try:
        if not llm_service or not llm_service.is_available():
            return jsonify({'error': 'LLM Service not available'}), 503
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        model_name = data.get('model_name')
        if not model_name:
            return jsonify({'error': 'model_name is required'}), 400
        
        # Validate model exists
        available_models = llm_service.get_available_models()
        if model_name not in available_models:
            return jsonify({
                'error': f'Model "{model_name}" not available',
                'available_models': available_models
            }), 400
        
        # Switch the model
        switched_model = llm_service.switch_model(model_name)
        
        return jsonify({
            'status': 'success',
            'current_model': switched_model,
            'message': f'Successfully switched to {switched_model}'
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to switch model: {str(e)}'}), 500

@model_api_bp.route('/current', methods=['GET'])
@api_login_required
def get_current_model():
    """Get currently active model"""
    try:
        if not llm_service or not llm_service.is_available():
            return jsonify({'error': 'LLM Service not available'}), 503
        
        current_model = llm_service.get_current_model()
        
        return jsonify({
            'current_model': current_model,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get current model: {str(e)}'}), 500