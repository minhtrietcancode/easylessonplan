"""
API Routes Module
Centralizes all API route definitions and connects them to the Flask app.
"""

from flask import Blueprint, jsonify
from backend.api.auth_api import AuthAPI
from backend.api.user_api import UserAPI

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


class APIRoutes:
    """Route handlers that connect API classes to Flask routes"""
    
    # === Authentication API Routes ===
    
    @staticmethod
    def auth_user_info():
        """GET /api/auth/user - Get current user information"""
        response_data, status_code = AuthAPI.get_user_info()
        return jsonify(response_data), status_code
    
    @staticmethod
    def auth_status():
        """GET /api/auth/status - Check authentication status"""
        response_data, status_code = AuthAPI.check_auth_status()
        return jsonify(response_data), status_code
    
    @staticmethod
    def auth_validate():
        """GET /api/auth/validate - Validate current session"""
        response_data, status_code = AuthAPI.validate_session()
        return jsonify(response_data), status_code
    
    @staticmethod
    def auth_get_preferences():
        """GET /api/auth/preferences - Get user preferences"""
        response_data, status_code = AuthAPI.get_user_preferences()
        return jsonify(response_data), status_code
    
    @staticmethod
    def auth_update_preferences():
        """PUT /api/auth/preferences - Update user preferences"""
        from flask import request
        
        try:
            preferences = request.get_json() or {}
            response_data, status_code = AuthAPI.update_user_preferences(preferences)
            return jsonify(response_data), status_code
        except Exception as e:
            response_data, status_code = AuthAPI.handle_exception(e, "Invalid request data")
            return jsonify(response_data), status_code
    
    # === User API Routes ===
    
    @staticmethod
    def user_profile():
        """GET /api/user/profile - Get user profile"""
        response_data, status_code = UserAPI.get_profile()
        return jsonify(response_data), status_code
    
    @staticmethod
    def user_update_profile():
        """PUT /api/user/profile - Update user profile"""
        from flask import request
        
        try:
            profile_data = request.get_json() or {}
            response_data, status_code = UserAPI.update_profile(profile_data)
            return jsonify(response_data), status_code
        except Exception as e:
            response_data, status_code = UserAPI.handle_exception(e, "Invalid request data")
            return jsonify(response_data), status_code
    
    @staticmethod
    def user_dashboard():
        """GET /api/user/dashboard - Get dashboard data"""
        response_data, status_code = UserAPI.get_dashboard_data()
        return jsonify(response_data), status_code
    
    @staticmethod
    def user_activity():
        """GET /api/user/activity - Get user activity log"""
        from flask import request
        
        try:
            limit = int(request.args.get('limit', 10))
            response_data, status_code = UserAPI.get_activity_log(limit)
            return jsonify(response_data), status_code
        except ValueError:
            response_data, status_code = UserAPI.error_response("Invalid limit parameter", 400)
            return jsonify(response_data), status_code
        except Exception as e:
            response_data, status_code = UserAPI.handle_exception(e, "Failed to get activity log")
            return jsonify(response_data), status_code
    
    @staticmethod
    def user_stats():
        """GET /api/user/stats - Get user statistics (placeholder)"""
        from flask import session
        
        try:
            user = session.get('user')
            if not user:
                response_data, status_code = UserAPI.error_response(
                    "Authentication required", 401, "AUTH_REQUIRED"
                )
                return jsonify(response_data), status_code
            
            # Placeholder stats
            stats = {
                'lessons_created': 0,
                'templates_used': 0,
                'total_time_saved': '0 hours',
                'subjects_covered': []
            }
            
            response_data, status_code = UserAPI.success_response(
                data=stats,
                message="User statistics retrieved"
            )
            return jsonify(response_data), status_code
            
        except Exception as e:
            response_data, status_code = UserAPI.handle_exception(e, "Failed to get user statistics")
            return jsonify(response_data), status_code


def register_api_routes():
    """Register all API routes to the blueprint"""
    
    # Authentication API routes
    api_bp.add_url_rule('/auth/user', 'auth_user_info', APIRoutes.auth_user_info, methods=['GET'])
    api_bp.add_url_rule('/auth/status', 'auth_status', APIRoutes.auth_status, methods=['GET'])
    api_bp.add_url_rule('/auth/validate', 'auth_validate', APIRoutes.auth_validate, methods=['GET'])
    api_bp.add_url_rule('/auth/preferences', 'auth_get_preferences', APIRoutes.auth_get_preferences, methods=['GET'])
    api_bp.add_url_rule('/auth/preferences', 'auth_update_preferences', APIRoutes.auth_update_preferences, methods=['PUT'])
    
    # User API routes
    api_bp.add_url_rule('/user/profile', 'user_profile', APIRoutes.user_profile, methods=['GET'])
    api_bp.add_url_rule('/user/profile', 'user_update_profile', APIRoutes.user_update_profile, methods=['PUT'])
    api_bp.add_url_rule('/user/dashboard', 'user_dashboard', APIRoutes.user_dashboard, methods=['GET'])
    api_bp.add_url_rule('/user/activity', 'user_activity', APIRoutes.user_activity, methods=['GET'])
    api_bp.add_url_rule('/user/stats', 'user_stats', APIRoutes.user_stats, methods=['GET'])


# Register routes when module is imported
register_api_routes()