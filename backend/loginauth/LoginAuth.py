"""
Authentication Service Module
Handles Google OAuth authentication and user session management.
"""

import os
import functools
from flask import Blueprint, request, redirect, session, url_for, jsonify, current_app
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.exceptions
from .AuthConfig import AuthConfig

# Set OAuth environment variable based on config
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' if AuthConfig.OAUTHLIB_INSECURE_TRANSPORT else '0'

# Create Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(f):
    """
    Decorator to require login for certain routes.
    Redirects to login page if user is not authenticated.
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


class AuthService:
    """Service class for handling authentication operations"""
    
    @staticmethod
    def create_oauth_flow():
        """Create and configure the Google OAuth flow"""
        try:
            client_config = {
                "web": {
                    "client_id": AuthConfig.GOOGLE_CLIENT_ID,
                    "client_secret": AuthConfig.GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [AuthConfig.get_redirect_uri()]
                }
            }
            
            flow = Flow.from_client_config(
                client_config,
                scopes=[
                    "https://www.googleapis.com/auth/userinfo.profile",
                    "https://www.googleapis.com/auth/userinfo.email",
                    "openid"
                ]
            )
            
            flow.redirect_uri = AuthConfig.get_redirect_uri()
            return flow
            
        except Exception as e:
            current_app.logger.error(f"Failed to create OAuth flow: {e}")
            raise
    
    @staticmethod
    def verify_and_extract_user_info(credentials):
        """
        Verify the OAuth token and extract user information.
        Returns user info dict or raises exception.
        """
        try:
            request_session = google_requests.Request()
            
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                credentials.id_token, 
                request_session, 
                AuthConfig.GOOGLE_CLIENT_ID
            )
            
            # Extract user information
            user_info = {
                'id': idinfo['sub'],
                'name': idinfo['name'],
                'email': idinfo['email'],
                'picture': idinfo.get('picture', ''),
                'verified_email': idinfo.get('email_verified', False)
            }
            
            current_app.logger.info(f"User authenticated: {user_info['email']}")
            return user_info
            
        except google.auth.exceptions.GoogleAuthError as e:
            current_app.logger.error(f"Google auth error: {e}")
            raise
        except Exception as e:
            current_app.logger.error(f"Token verification failed: {e}")
            raise
    
    @staticmethod
    def store_user_session(user_info):
        """Store user information in session"""
        session['user'] = user_info
        session.permanent = AuthConfig.SESSION_PERMANENT
    
    @staticmethod
    def clear_user_session():
        """Clear user session data"""
        session.clear()
    
    @staticmethod
    def get_current_user():
        """Get current user from session, returns None if not logged in"""
        return session.get('user')


class AuthRoutes:
    """Route handlers for authentication endpoints"""
    
    @staticmethod
    def login():
        """Initiate Google OAuth login process"""
        try:
            flow = AuthService.create_oauth_flow()
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            
            # Store state for CSRF protection
            session['oauth_state'] = state
            
            return redirect(authorization_url)
            
        except Exception as e:
            current_app.logger.error(f"Login initiation failed: {e}")
            return jsonify({
                'error': 'Failed to initiate login process',
                'details': str(e) if current_app.debug else None
            }), 500
    
    @staticmethod
    def callback():
        """Handle Google OAuth callback and complete authentication"""
        try:
            # Verify state parameter for CSRF protection
            received_state = request.args.get('state')
            stored_state = session.get('oauth_state')
            
            if not received_state or received_state != stored_state:
                current_app.logger.warning("OAuth state mismatch detected")
                return jsonify({'error': 'Invalid authentication state'}), 400
            
            # Handle OAuth error responses
            if 'error' in request.args:
                error = request.args.get('error')
                current_app.logger.warning(f"OAuth error: {error}")
                return redirect(url_for('index', error='auth_cancelled'))
            
            # Create flow and fetch token
            flow = AuthService.create_oauth_flow()
            flow.fetch_token(authorization_response=request.url)
            
            # Verify token and get user info
            user_info = AuthService.verify_and_extract_user_info(flow.credentials)
            
            # Store user in session
            AuthService.store_user_session(user_info)
            
            # Clean up OAuth state
            session.pop('oauth_state', None)
            
            # Redirect to EasyLesson page
            return redirect(url_for('easylesson'))
            
        except google.auth.exceptions.GoogleAuthError as e:
            current_app.logger.error(f"Google authentication error: {e}")
            return jsonify({
                'error': 'Google authentication failed',
                'details': str(e) if current_app.debug else None
            }), 400
            
        except Exception as e:
            current_app.logger.error(f"Authentication callback failed: {e}")
            return jsonify({
                'error': 'Authentication process failed',
                'details': str(e) if current_app.debug else None
            }), 500
    
    @staticmethod
    def logout():
        """Logout user and redirect to home page"""
        user = AuthService.get_current_user()
        if user:
            current_app.logger.info(f"User logged out: {user.get('email', 'unknown')}")
        
        AuthService.clear_user_session()
        return redirect(url_for('index'))


def register_auth_routes():
    """Register all authentication routes to the blueprint"""
    auth_bp.add_url_rule('/login', 'login', AuthRoutes.login, methods=['GET'])
    auth_bp.add_url_rule('/callback', 'callback', AuthRoutes.callback, methods=['GET'])
    auth_bp.add_url_rule('/logout', 'logout', AuthRoutes.logout, methods=['GET', 'POST'])


# Register routes when module is imported
register_auth_routes()