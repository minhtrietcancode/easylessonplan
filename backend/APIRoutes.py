"""
API Routes Module
Centralizes all API route definitions and connects them directly to API classes.
"""

from flask import Blueprint
from backend.api.auth_api import AuthAPI
from backend.api.user_api import UserAPI
from backend.api.llm_api import LlmAPI

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


def register_api_routes():
    """
    Register all API routes to the blueprint.
    Routes are organized by functionality with clear comments for easy maintenance.
    """
    
    ###########################################################################################
    #                           AUTHENTICATION API ROUTES                                    #
    ###########################################################################################
    
    # User information and session management
    api_bp.add_url_rule('/auth/user', 'auth_user_info', 
                       AuthAPI.get_user_info, methods=['GET'])
    
    api_bp.add_url_rule('/auth/status', 'auth_status', 
                       AuthAPI.check_auth_status, methods=['GET'])
    
    api_bp.add_url_rule('/auth/validate', 'auth_validate', 
                       AuthAPI.validate_session, methods=['GET'])
    
    # User preferences
    api_bp.add_url_rule('/auth/preferences', 'auth_get_preferences', 
                       AuthAPI.get_user_preferences, methods=['GET'])
    
    api_bp.add_url_rule('/auth/preferences', 'auth_update_preferences', 
                       AuthAPI.update_user_preferences, methods=['PUT'])
    
    ###########################################################################################
    #                              USER API ROUTES                                           #
    ###########################################################################################
    
    # User profile management
    api_bp.add_url_rule('/user/profile', 'user_profile', 
                       UserAPI.get_profile, methods=['GET'])
    
    api_bp.add_url_rule('/user/profile', 'user_update_profile', 
                       UserAPI.update_profile, methods=['PUT'])
    
    # Dashboard and statistics
    api_bp.add_url_rule('/user/dashboard', 'user_dashboard', 
                       UserAPI.get_dashboard_data, methods=['GET'])
    
    api_bp.add_url_rule('/user/activity', 'user_activity', 
                       UserAPI.get_activity_log, methods=['GET'])
    
    api_bp.add_url_rule('/user/stats', 'user_stats', 
                       UserAPI.get_user_stats, methods=['GET'])
    
    ###########################################################################################
    #                             LLM FUNCTIONALITY API ROUTES                               #
    ###########################################################################################
    
    # Model management
    api_bp.add_url_rule('/llm/models', 'llm_get_models', 
                       LlmAPI.get_available_models, methods=['GET'])
    
    api_bp.add_url_rule('/llm/models', 'llm_set_model', 
                       LlmAPI.set_current_model, methods=['PUT'])
    
    # Chat functionality
    api_bp.add_url_rule('/llm/chat', 'llm_chat', 
                       LlmAPI.send_chat_message, methods=['POST'])


# Register routes when module is imported
register_api_routes()