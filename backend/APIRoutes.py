# File: backend/APIRoutes.py
"""
API Routes Module
Centralizes all route registration for both auth and LLM functionality.
Makes it easy to see and manage all routes in one place.
"""

from flask import Blueprint
from backend.api.AuthAPI import AuthAPI
from backend.api.LlmAPI import LlmAPI

# Create blueprints
auth_bp = Blueprint('auth', __name__)
llm_bp = Blueprint('llm', __name__)

###########################################################################################
#                           AUTHENTICATION ROUTES                                        #
###########################################################################################

# OAuth flow routes
auth_bp.add_url_rule('/auth/login', view_func=AuthAPI.login, methods=['GET'])
auth_bp.add_url_rule('/auth/callback', view_func=AuthAPI.callback, methods=['GET'])
auth_bp.add_url_rule('/auth/logout', view_func=AuthAPI.logout, methods=['GET', 'POST'])

# User info route (moved from /api/auth/user to /auth/user)
auth_bp.add_url_rule('/auth/user', view_func=AuthAPI.get_user_info, methods=['GET'])

###########################################################################################
#                             LLM ROUTES                                                 #
###########################################################################################

# Model management routes
llm_bp.add_url_rule('/llm/models', view_func=LlmAPI.get_available_models, methods=['GET'])
llm_bp.add_url_rule('/llm/models', view_func=LlmAPI.set_current_model, methods=['PUT'])
llm_bp.add_url_rule('/llm/current', view_func=LlmAPI.get_current_model, methods=['GET'])

# Chat functionality route
llm_bp.add_url_rule('/llm/chat', view_func=LlmAPI.send_chat_message, methods=['POST'])