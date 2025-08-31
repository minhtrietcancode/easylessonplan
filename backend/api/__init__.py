"""
API Module Initialization
Registers all API blueprints and provides centralized API configuration
"""

from flask import Blueprint
from .auth_api import auth_api_bp
from .chat_api import chat_api_bp
from .model_api import model_api_bp
from .health_api import health_api_bp

def register_api_blueprints(app):
    """Register all API blueprints with the Flask app"""
    
    # API version prefix
    api_prefix = '/api/v1'
    
    # Register blueprints
    app.register_blueprint(auth_api_bp, url_prefix=f'{api_prefix}/auth')
    app.register_blueprint(chat_api_bp, url_prefix=f'{api_prefix}/chat')
    app.register_blueprint(model_api_bp, url_prefix=f'{api_prefix}/models')
    app.register_blueprint(health_api_bp, url_prefix=f'{api_prefix}/health')
    
    print(f"✅ API blueprints registered with prefix: {api_prefix}")

# Export for easy importing
__all__ = ['register_api_blueprints']