"""
User API Module
Handles user-related API endpoints and operations.
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
import datetime

# Initialize auth service
auth_service = AuthService(AuthConfig)


class UserAPI(BaseAPI):
    """API handler for user operations"""
    
    @classmethod
    def get_profile(cls):
        """
        GET /api/user/profile - Get detailed user profile information
        
        Returns:
            Flask response with user profile data
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
            
            # Enhanced profile data
            profile_data = {
                **cls.sanitize_user_data(user),
                'joined_date': None,  # Placeholder for user registration date
                'last_active': datetime.datetime.utcnow().isoformat(),
                'profile_complete': cls._check_profile_completeness(user),
                'account_status': 'active'
            }
            
            response_data, status_code = cls.success_response(
                data=profile_data,
                message="Profile retrieved successfully"
            )
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to retrieve user profile")
            return jsonify(response_data), status_code
    
    @classmethod
    def update_profile(cls):
        """
        PUT /api/user/profile - Update user profile information
        
        Returns:
            Flask response confirming update
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
            
            # Get profile data from request
            profile_data = request.get_json() or {}
            
            # Validate updatable fields
            updatable_fields = ['name', 'picture']  # Only allow certain fields to be updated
            invalid_fields = [field for field in profile_data.keys() if field not in updatable_fields]
            
            if invalid_fields:
                response_data, status_code = cls.error_response(
                    message=f"Cannot update fields: {', '.join(invalid_fields)}",
                    status_code=400,
                    error_code="INVALID_FIELDS"
                )
                return jsonify(response_data), status_code
            
            # Update session data
            for field, value in profile_data.items():
                if field in updatable_fields and value is not None:
                    user[field] = value
            
            # Update session
            session['user'] = user
            
            current_app.logger.info(f"User {user.get('id')} updated profile")
            
            response_data, status_code = cls.success_response(
                data=cls.sanitize_user_data(user),
                message="Profile updated successfully"
            )
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to update user profile")
            return jsonify(response_data), status_code
    
    @classmethod
    def get_dashboard_data(cls):
        """
        GET /api/user/dashboard - Get dashboard data for authenticated user
        
        Returns:
            Flask response with dashboard information
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
            
            response_data, status_code = cls.success_response(
                data=dashboard_data,
                message="Dashboard data retrieved successfully"
            )
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to retrieve dashboard data")
            return jsonify(response_data), status_code
    
    @classmethod
    def get_activity_log(cls):
        """
        GET /api/user/activity - Get user activity log
        
        Returns:
            Flask response with activity data
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
            
            # Get limit from query parameters
            try:
                limit = int(request.args.get('limit', 10))
            except ValueError:
                response_data, status_code = cls.error_response(
                    message="Invalid limit parameter", 
                    status_code=400,
                    error_code="INVALID_LIMIT"
                )
                return jsonify(response_data), status_code
            
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
            
            response_data, status_code = cls.success_response(
                data={
                    'activities': activities[:limit],
                    'total_count': len(activities),
                    'has_more': len(activities) > limit
                },
                message="Activity log retrieved successfully"
            )
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to retrieve activity log")
            return jsonify(response_data), status_code
    
    @classmethod
    def get_user_stats(cls):
        """
        GET /api/user/stats - Get user statistics
        
        Returns:
            Flask response with user statistics
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
            
            # Placeholder stats
            stats = {
                'lessons_created': 0,
                'templates_used': 0,
                'total_time_saved': '0 hours',
                'subjects_covered': []
            }
            
            response_data, status_code = cls.success_response(
                data=stats,
                message="User statistics retrieved"
            )
            
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = cls.handle_exception(e, "Failed to get user statistics")
            return jsonify(response_data), status_code
    
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