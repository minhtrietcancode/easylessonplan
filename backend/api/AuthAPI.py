"""
Authentication API Module
Handles authentication status and user info API endpoints (JSON responses).
This is separate from OAuth routes which handle redirects.
"""

from flask import session, request, current_app, jsonify
from .BaseAPI import BaseAPI
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