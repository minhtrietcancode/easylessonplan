"""
Authentication API Module
Handles all authentication-related API endpoints and logic.
"""

from flask import session, request, current_app
from .base_api import BaseAPI
import sys
import os

# Add the parent directory to the path to import loginauth
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loginauth import AuthService

from typing import Dict, Any, Tuple


class AuthAPI(BaseAPI):
    """API handler for authentication operations"""
    
    @classmethod
    def get_user_info(cls) -> Tuple[Dict, int]:
        """
        Get current user information from session
        
        Returns:
            API response with user data
        """
        try:
            user = AuthService.get_current_user()
            
            if user:
                sanitized_user = cls.sanitize_user_data(user)
                return cls.success_response(
                    data={
                        'user': sanitized_user,
                        'authenticated': True
                    },
                    message="User information retrieved successfully"
                )
            else:
                return cls.success_response(
                    data={
                        'user': None,
                        'authenticated': False
                    },
                    message="No authenticated user"
                )
                
        except Exception as e:
            return cls.handle_exception(e, "Failed to retrieve user information")
    
    @classmethod
    def check_auth_status(cls) -> Tuple[Dict, int]:
        """
        Check if user is currently authenticated
        
        Returns:
            API response with authentication status
        """
        try:
            user = AuthService.get_current_user()
            
            return cls.success_response(
                data={
                    'authenticated': user is not None,
                    'user_id': user.get('id') if user else None,
                    'session_active': 'user' in session
                },
                message="Authentication status checked"
            )
            
        except Exception as e:
            return cls.handle_exception(e, "Failed to check authentication status")
    
    @classmethod
    def validate_session(cls) -> Tuple[Dict, int]:
        """
        Validate current user session
        
        Returns:
            API response with session validation result
        """
        try:
            user = AuthService.get_current_user()
            
            if not user:
                return cls.error_response(
                    message="No active session found",
                    status_code=401,
                    error_code="NO_SESSION"
                )
            
            # Additional session validation can be added here
            # For example, checking session expiry, token refresh, etc.
            
            return cls.success_response(
                data={
                    'valid': True,
                    'user_id': user.get('id'),
                    'expires_at': None  # Can be implemented later
                },
                message="Session is valid"
            )
            
        except Exception as e:
            return cls.handle_exception(e, "Failed to validate session")
    
    @classmethod
    def get_user_preferences(cls) -> Tuple[Dict, int]:
        """
        Get user preferences (placeholder for future implementation)
        
        Returns:
            API response with user preferences
        """
        try:
            user = AuthService.get_current_user()
            
            if not user:
                return cls.error_response(
                    message="Authentication required",
                    status_code=401,
                    error_code="AUTH_REQUIRED"
                )
            
            # Placeholder for user preferences
            # This can be expanded to fetch from database
            preferences = {
                'theme': 'light',
                'language': 'en',
                'notifications': True,
                'auto_save': True
            }
            
            return cls.success_response(
                data=preferences,
                message="User preferences retrieved"
            )
            
        except Exception as e:
            return cls.handle_exception(e, "Failed to retrieve user preferences")
    
    @classmethod
    def update_user_preferences(cls, preferences: Dict[str, Any]) -> Tuple[Dict, int]:
        """
        Update user preferences (placeholder for future implementation)
        
        Args:
            preferences: Dictionary of preference updates
            
        Returns:
            API response confirming update
        """
        try:
            user = AuthService.get_current_user()
            
            if not user:
                return cls.error_response(
                    message="Authentication required",
                    status_code=401,
                    error_code="AUTH_REQUIRED"
                )
            
            # Validate preference data
            allowed_preferences = ['theme', 'language', 'notifications', 'auto_save']
            invalid_prefs = [key for key in preferences.keys() if key not in allowed_preferences]
            
            if invalid_prefs:
                return cls.error_response(
                    message=f"Invalid preference keys: {', '.join(invalid_prefs)}",
                    status_code=400,
                    error_code="INVALID_PREFERENCES"
                )
            
            # Placeholder for database update
            # In future: save preferences to database
            
            current_app.logger.info(f"User {user.get('id')} updated preferences: {preferences}")
            
            return cls.success_response(
                data=preferences,
                message="Preferences updated successfully"
            )
            
        except Exception as e:
            return cls.handle_exception(e, "Failed to update user preferences")