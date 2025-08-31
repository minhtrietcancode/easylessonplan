"""
Health Check API Routes
Provides system health, status monitoring, and diagnostic endpoints
"""

from flask import Blueprint, jsonify
import sys
import os

health_api_bp = Blueprint('health_api', __name__)

# This will be injected by the main app
llm_service = None

def set_llm_service(service):
    """Set the LLM service instance"""
    global llm_service
    llm_service = service

@health_api_bp.route('/status', methods=['GET'])
def health_status():
    """Comprehensive health check"""
    try:
        # Basic system info
        health_data = {
            'status': 'healthy',
            'service': 'EasyLesson API',
            'python_version': sys.version.split()[0],
            'platform': sys.platform
        }
        
        # LLM service status
        if llm_service:
            health_data.update({
                'llm_service_status': 'available' if llm_service.is_available() else 'unavailable',
                'available_models': llm_service.get_available_models() if llm_service.is_available() else [],
                'current_model': llm_service.get_current_model() if llm_service.is_available() else None
            })
        else:
            health_data.update({
                'llm_service_status': 'not_initialized',
                'available_models': [],
                'current_model': None
            })
        
        return jsonify(health_data)
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@health_api_bp.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint"""
    return jsonify({'message': 'pong', 'status': 'success'})

@health_api_bp.route('/dependencies', methods=['GET'])
def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        dependencies = {
            'flask': True,
            'flask_cors': True,
            'llm_manager': llm_service is not None if llm_service else False
        }
        
        # Test imports
        try:
            import flask
            dependencies['flask_version'] = flask.__version__
        except ImportError:
            dependencies['flask'] = False
        
        try:
            import flask_cors
            dependencies['flask_cors'] = True
        except ImportError:
            dependencies['flask_cors'] = False
        
        all_ok = all(dep for key, dep in dependencies.items() if isinstance(dep, bool))
        
        return jsonify({
            'dependencies': dependencies,
            'all_dependencies_ok': all_ok,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500