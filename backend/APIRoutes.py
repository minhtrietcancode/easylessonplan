"""
API Routes Module
Centralizes all API route definitions and connects them directly to API classes.
"""

from flask import Blueprint
from backend.api.AuthAPI import AuthAPI
from backend.api.UserAPI import UserAPI
from backend.api.LlmAPI import LlmAPI

# Create API blueprint without url_prefix
api_bp = Blueprint('api', __name__)

# Route configuration dictionary
ROUTES = {
    ###########################################################################################
    #                           AUTHENTICATION API ROUTES                                    #
    ###########################################################################################
    AuthAPI: [
        # User information and session management
        {'path': '/api/auth/user', 'endpoint': 'auth_user_info', 'method': 'get_user_info', 'methods': ['GET']},
        {'path': '/api/auth/status', 'endpoint': 'auth_status', 'method': 'check_auth_status', 'methods': ['GET']},
        {'path': '/api/auth/validate', 'endpoint': 'auth_validate', 'method': 'validate_session', 'methods': ['GET']},
        
        # User preferences
        {'path': '/api/auth/preferences', 'endpoint': 'auth_get_preferences', 'method': 'get_user_preferences', 'methods': ['GET']},
        {'path': '/api/auth/preferences', 'endpoint': 'auth_update_preferences', 'method': 'update_user_preferences', 'methods': ['PUT']},
    ],
    
    ###########################################################################################
    #                              USER API ROUTES                                           #
    ###########################################################################################
    UserAPI: [
        # User profile management
        {'path': '/api/user/profile', 'endpoint': 'user_profile', 'method': 'get_profile', 'methods': ['GET']},
        {'path': '/api/user/profile', 'endpoint': 'user_update_profile', 'method': 'update_profile', 'methods': ['PUT']},
        
        # Dashboard and statistics
        {'path': '/api/user/dashboard', 'endpoint': 'user_dashboard', 'method': 'get_dashboard_data', 'methods': ['GET']},
        {'path': '/api/user/activity', 'endpoint': 'user_activity', 'method': 'get_activity_log', 'methods': ['GET']},
        {'path': '/api/user/stats', 'endpoint': 'user_stats', 'method': 'get_user_stats', 'methods': ['GET']},
    ],
    
    ###########################################################################################
    #                             LLM FUNCTIONALITY API ROUTES                               #
    ###########################################################################################
    LlmAPI: [
        # Model management
        {'path': '/api/llm/models', 'endpoint': 'llm_get_models', 'method': 'get_available_models', 'methods': ['GET']},
        {'path': '/api/llm/models', 'endpoint': 'llm_set_model', 'method': 'set_current_model', 'methods': ['PUT']},
        
        # Chat functionality
        {'path': '/api/llm/chat', 'endpoint': 'llm_chat', 'method': 'send_chat_message', 'methods': ['POST']},
    ],
}


def register_api_routes():
    """
    Register all API routes to the blueprint using the ROUTES configuration.
    This approach eliminates repetitive add_url_rule calls and makes route management cleaner.
    """
    for api_class, routes in ROUTES.items():
        for route_config in routes:
            api_bp.add_url_rule(
                rule=route_config['path'],
                endpoint=route_config['endpoint'],
                view_func=getattr(api_class, route_config['method']),
                methods=route_config['methods']
            )


# Register routes when module is imported
register_api_routes()