# File: backend\api\BaseAPI.py
"""
Base API Module
Provides common functionality and utilities for all API endpoints.
"""

from flask import jsonify, current_app
import traceback
from typing import Dict, Any, Tuple, Optional


class BaseAPI:
    """Base class for all API handlers with common utilities"""
    
    @staticmethod
    def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> Tuple[Dict, int]:
        """
        Create a standardized success response
        
        Args:
            data: Response data
            message: Success message
            status_code: HTTP status code
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        response = {
            'success': True,
            'message': message,
            'data': data
        }
        return response, status_code
    
    @staticmethod
    def error_response(message: str, status_code: int = 400, error_code: str = None, details: Any = None) -> Tuple[Dict, int]:
        """
        Create a standardized error response
        
        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Custom error code
            details: Additional error details (only in debug mode)
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        response = {
            'success': False,
            'message': message,
            'error_code': error_code
        }
        
        # Only include details in debug mode
        if details and current_app.debug:
            response['details'] = details
            
        return response, status_code
    
    @staticmethod
    def handle_exception(e: Exception, default_message: str = "An error occurred") -> Tuple[Dict, int]:
        """
        Handle exceptions and return appropriate error response
        
        Args:
            e: Exception object
            default_message: Default error message
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        current_app.logger.error(f"API Exception: {str(e)}")
        
        if current_app.debug:
            current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        
        return BaseAPI.error_response(
            message=default_message,
            status_code=500,
            details=str(e) if current_app.debug else None
        )
    
    @staticmethod
    def validate_required_fields(data: Dict, required_fields: list) -> Optional[Tuple[Dict, int]]:
        """
        Validate that required fields are present in request data
        
        Args:
            data: Request data dictionary
            required_fields: List of required field names
            
        Returns:
            Error response tuple if validation fails, None if successful
        """
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        
        if missing_fields:
            return BaseAPI.error_response(
                message=f"Missing required fields: {', '.join(missing_fields)}",
                status_code=400,
                error_code="MISSING_FIELDS"
            )
        
        return None
    
    @staticmethod
    def sanitize_user_data(user_data: Dict) -> Dict:
        """
        Sanitize user data for safe API responses
        
        Args:
            user_data: Raw user data from session
            
        Returns:
            Sanitized user data
        """
        if not user_data:
            return {}
        
        return {
            'id': user_data.get('id'),
            'name': user_data.get('name'),
            'email': user_data.get('email'),
            'picture': user_data.get('picture', ''),
            'verified_email': user_data.get('verified_email', False)
        }