"""
Authentication API Routes
Handles user authentication, session management, and user info endpoints
"""

from flask import Blueprint, session, jsonify, request
from functools import wraps

auth_api_bp = Blueprint('auth_api', __name__)

def api_login_required(f):
    """Decorator for API endpoints that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required', 'authenticated': False}), 401
        return f(*args, **kwargs)
    return decorated_function

@auth_api_bp.route('/user', methods=['GET'])
def get_user_info():
    """Get current user information"""
    try:
        user = session.get('user')
        
        return jsonify({
            'user': user,
            'authenticated': user is not None,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'authenticated': False,
            'status': 'error'
        }), 500

@auth_api_bp.route('/logout', methods=['POST'])
@api_login_required
def logout_user():
    """Logout current user"""
    try:
        user_name = session.get('user', {}).get('name', 'User')
        session.clear()
        
        return jsonify({
            'message': f'{user_name} logged out successfully',
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@auth_api_bp.route('/session/validate', methods=['GET'])
def validate_session():
    """Validate current session"""
    try:
        user = session.get('user')
        is_valid = user is not None
        
        return jsonify({
            'valid': is_valid,
            'user': user if is_valid else None,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'valid': False,
            'status': 'error'
        }), 500