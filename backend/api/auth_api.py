"""
Authentication API Module
Handles authentication status and user info API endpoints (JSON responses).
This is separate from OAuth routes which handle redirects.
"""

from flask import session, request, current_app, jsonify
from .base_api import BaseAPI
import sys
import os

# Add the parent directory to the path to import loginauth
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.auth.AuthService import AuthService
from backend.auth.AuthConfig import AuthConfig

from typing import Dict, Any, Tuple

# Initialize auth service
auth_service = AuthService(AuthConfig)


class AuthAPI(BaseAPI):
    """API handler for authentication status operations (JSON responses only)"""
    
    @classmethod
    def get_user_info(cls):
        """
        GET /api/auth/user - Get current user information from session
        
        Returns:
            Flask JSON response with user data
        """
        try:
            user = auth_service.get_current_user(session)
            
            if user:
                sanitized_user = cls.sanitize_user_data(user)
                response_data, status_code = cls.success_response(
                    data={
                        'user': sanitized_user,
                        'authenticated': True
                    },
                    message="User information retrieved successfully"
                )
            else:
                response_data, status_code = cls.success_response(
                    data={
                        'user': None,
                        'authenticated': False
                    },
                    message="No authenticated user"
                )
                
            return jsonify(response_data), status_code
                
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to retrieve user information")
            return jsonify(response_data), status_code
    
    @classmethod
    def check_auth_status(cls):
        """
        GET /api/auth/status - Check if user is currently authenticated
        
        Returns:
            Flask JSON response with authentication status
        """
        try:
            user = auth_service.get_current_user(session)
            
            response_data, status_code = cls.success_response(
                data={
                    'authenticated': user is not None,
                    'user_id': user.get('id') if user else None,
                    'session_active': 'user' in session
                },
                message="Authentication status checked"
            )
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to check authentication status")
            return jsonify(response_data), status_code
    
    @classmethod
    def validate_session(cls):
        """
        GET /api/auth/validate - Validate current user session
        
        Returns:
            Flask JSON response with session validation result
        """
        try:
            user = auth_service.get_current_user(session)
            
            if not user:
                response_data, status_code = cls.error_response(
                    message="No active session found",
                    status_code=401,
                    error_code="NO_SESSION"
                )
                return jsonify(response_data), status_code
            
            # Additional session validation can be added here
            # For example, checking session expiry, token refresh, etc.
            
            response_data, status_code = cls.success_response(
                data={
                    'valid': True,
                    'user_id': user.get('id'),
                    'expires_at': None  # Can be implemented later
                },
                message="Session is valid"
            )
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to validate session")
            return jsonify(response_data), status_code
    
    @classmethod
    def get_user_preferences(cls):
        """
        GET /api/auth/preferences - Get user preferences
        
        Returns:
            Flask JSON response with user preferences
        """
        try:
            user = auth_service.get_current_user(session)
            
            if not user:
                response_data, status_code = cls.error_response(
                    message="Authentication required",
                    status_code=401,
                    error_code="AUTH_REQUIRED"
                )
                return jsonify(response_data), status_code
            
            # Placeholder for user preferences
            # This can be expanded to fetch from database
            preferences = {
                'theme': 'light',
                'language': 'en',
                'notifications': True,
                'auto_save': True
            }
            
            response_data, status_code = cls.success_response(
                data=preferences,
                message="User preferences retrieved"
            )
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to retrieve user preferences")
            return jsonify(response_data), status_code
    
    @classmethod
    def update_user_preferences(cls):
        """
        PUT /api/auth/preferences - Update user preferences
        
        Returns:
            Flask JSON response confirming update
        """
        try:
            user = auth_service.get_current_user(session)
            
            if not user:
                response_data, status_code = cls.error_response(
                    message="Authentication required",
                    status_code=401,
                    error_code="AUTH_REQUIRED"
                )
                return jsonify(response_data), status_code
            
            # Get preferences from request
            preferences = request.get_json() or {}
            
            # Validate preference data
            allowed_preferences = ['theme', 'language', 'notifications', 'auto_save']
            invalid_prefs = [key for key in preferences.keys() if key not in allowed_preferences]
            
            if invalid_prefs:
                response_data, status_code = cls.error_response(
                    message=f"Invalid preference keys: {', '.join(invalid_prefs)}",
                    status_code=400,
                    error_code="INVALID_PREFERENCES"
                )
                return jsonify(response_data), status_code
            
            # Placeholder for database update
            # In future: save preferences to database
            
            current_app.logger.info(f"User {user.get('id')} updated preferences: {preferences}")
            
            response_data, status_code = cls.success_response(
                data=preferences,
                message="Preferences updated successfully"
            )
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to update user preferences")
            return jsonify(response_data), status_code