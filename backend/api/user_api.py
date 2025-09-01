"""
User API Module
Handles user-related API endpoints and operations.
"""

from flask import session, current_app
from .base_api import BaseAPI
import sys
import os

# Add the parent directory to the path to import loginauth
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.loginauth.LoginAuth import AuthService

from typing import Dict, Any, Tuple
import datetime


class UserAPI(BaseAPI):
    """API handler for user operations"""
    
    @classmethod
    def get_profile(cls) -> Tuple[Dict, int]:
        """
        Get detailed user profile information
        
        Returns:
            API response with user profile data
        """
        try:
            user = AuthService.get_current_user()
            
            if not user:
                return cls.error_response(
                    message="Authentication required",
                    status_code=401,
                    error_code="AUTH_REQUIRED"
                )
            
            # Enhanced profile data
            profile_data = {
                **cls.sanitize_user_data(user),
                'joined_date': None,  # Placeholder for user registration date
                'last_active': datetime.datetime.utcnow().isoformat(),
                'profile_complete': cls._check_profile_completeness(user),
                'account_status': 'active'
            }
            
            return cls.success_response(
                data=profile_data,
                message="Profile retrieved successfully"
            )
            
        except Exception as e:
            return cls.handle_exception(e, "Failed to retrieve user profile")
    
    @classmethod
    def update_profile(cls, profile_data: Dict[str, Any]) -> Tuple[Dict, int]:
        """
        Update user profile information
        
        Args:
            profile_data: Dictionary containing profile updates
            
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
            
            # Validate updatable fields
            updatable_fields = ['name', 'picture']  # Only allow certain fields to be updated
            invalid_fields = [field for field in profile_data.keys() if field not in updatable_fields]
            
            if invalid_fields:
                return cls.error_response(
                    message=f"Cannot update fields: {', '.join(invalid_fields)}",
                    status_code=400,
                    error_code="INVALID_FIELDS"
                )
            
            # Update session data
            for field, value in profile_data.items():
                if field in updatable_fields and value is not None:
                    user[field] = value
            
            # Update session
            session['user'] = user
            
            current_app.logger.info(f"User {user.get('id')} updated profile")
            
            return cls.success_response(
                data=cls.sanitize_user_data(user),
                message="Profile updated successfully"
            )
            
        except Exception as e:
            return cls.handle_exception(e, "Failed to update user profile")
    
    @classmethod
    def get_dashboard_data(cls) -> Tuple[Dict, int]:
        """
        Get dashboard data for authenticated user
        
        Returns:
            API response with dashboard information
        """
        try:
            user = AuthService.get_current_user()
            
            if not user:
                return cls.error_response(
                    message="Authentication required",
                    status_code=401,
                    error_code="AUTH_REQUIRED"
                )
            
            # Placeholder dashboard data
            dashboard_data = {
                'user': cls.sanitize_user_data(user),
                'stats': {
                    'total_lessons': 0,
                    'recent_lessons': [],
                    'favorite_subjects': [],
                    'usage_this_month': 0
                },
                'quick_actions': [
                    {'id': 'new_lesson', 'title': 'Create New Lesson', 'icon': 'fas fa-plus'},
                    {'id': 'browse_templates', 'title': 'Browse Templates', 'icon': 'fas fa-search'},
                    {'id': 'recent_work', 'title': 'Recent Work', 'icon': 'fas fa-history'}
                ],
                'notifications': [],
                'last_login': datetime.datetime.utcnow().isoformat()
            }
            
            return cls.success_response(
                data=dashboard_data,
                message="Dashboard data retrieved successfully"
            )
            
        except Exception as e:
            return cls.handle_exception(e, "Failed to retrieve dashboard data")
    
    @classmethod
    def get_activity_log(cls, limit: int = 10) -> Tuple[Dict, int]:
        """
        Get user activity log
        
        Args:
            limit: Maximum number of activities to return
            
        Returns:
            API response with activity data
        """
        try:
            user = AuthService.get_current_user()
            
            if not user:
                return cls.error_response(
                    message="Authentication required",
                    status_code=401,
                    error_code="AUTH_REQUIRED"
                )
            
            # Placeholder activity data
            # In future, this would fetch from database
            activities = [
                {
                    'id': 1,
                    'type': 'login',
                    'description': 'Logged in to EasyLesson',
                    'timestamp': datetime.datetime.utcnow().isoformat(),
                    'details': {}
                }
            ]
            
            return cls.success_response(
                data={
                    'activities': activities[:limit],
                    'total_count': len(activities),
                    'has_more': len(activities) > limit
                },
                message="Activity log retrieved successfully"
            )
            
        except Exception as e:
            return cls.handle_exception(e, "Failed to retrieve activity log")
    
    @staticmethod
    def _check_profile_completeness(user: Dict) -> bool:
        """
        Check if user profile is complete
        
        Args:
            user: User data dictionary
            
        Returns:
            True if profile is complete, False otherwise
        """
        required_fields = ['name', 'email']
        return all(user.get(field) for field in required_fields)