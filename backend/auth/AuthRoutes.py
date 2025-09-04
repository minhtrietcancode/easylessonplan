"""
OAuth Authentication Routes Module
Handles Google OAuth authentication flow with redirects.
This module only handles the OAuth flow - API endpoints are in backend/api/
"""

from flask import Blueprint, request, redirect, session, url_for, jsonify, current_app
from .AuthService import AuthService
from .AuthConfig import AuthConfig
import google.auth.exceptions

# Create Blueprint for OAuth routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Initialize auth service
auth_service = AuthService(AuthConfig)


class AuthRoutes:
    def __init__(self, auth_service, auth_bp):
        self.auth_service = auth_service
        self.auth_bp = auth_bp
        self.register_routes()

    def login(self):
        """
        GET /auth/login - Initiate Google OAuth login process
        Redirects user to Google OAuth page
        """
        try:
            flow = self.auth_service.create_oauth_flow()
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            
            # Store state for CSRF protection
            session['oauth_state'] = state
            
            current_app.logger.info("OAuth login initiated")
            return redirect(authorization_url)
            
        except Exception as e:
            current_app.logger.error(f"Login initiation failed: {e}")
            return jsonify({
                'error': 'Failed to initiate login process',
                'details': str(e) if current_app.debug else None
            }), 500

    def callback(self):
        """
        GET /auth/callback - Handle Google OAuth callback
        Google redirects back to this endpoint after user authentication
        """
        try:
            # Verify state parameter for CSRF protection
            received_state = request.args.get('state')
            stored_state = session.get('oauth_state')
            
            if not received_state or received_state != stored_state:
                current_app.logger.warning("OAuth state mismatch detected")
                return jsonify({'error': 'Invalid authentication state'}), 400
            
            # Handle OAuth error responses from Google
            if 'error' in request.args:
                error = request.args.get('error')
                current_app.logger.warning(f"OAuth error: {error}")
                return redirect(url_for('index', error='auth_cancelled'))
            
            # Complete OAuth flow
            flow = self.auth_service.create_oauth_flow()
            flow.fetch_token(authorization_response=request.url)
            
            # Verify token and get user info
            user_info = self.auth_service.verify_token_and_get_user(flow.credentials)
            
            # Store user in session
            self.auth_service.store_user_in_session(session, user_info)
            
            # Clean up OAuth state
            session.pop('oauth_state', None)
            
            current_app.logger.info(f"User authenticated successfully: {user_info['email']}")
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

    def logout(self):
        """
        GET/POST /auth/logout - Logout user and redirect to home page
        Clears user session and redirects to home
        """
        user = self.auth_service.get_current_user(session)
        if user:
            current_app.logger.info(f"User logged out: {user.get('email', 'unknown')}")
        else:
            current_app.logger.info("Logout attempted with no active session")
        
        self.auth_service.clear_session(session)
        return redirect(url_for('index'))

    def register_routes(self):
        self.auth_bp.add_url_rule('/login', view_func=self.login, methods=['GET'])
        self.auth_bp.add_url_rule('/callback', view_func=self.callback, methods=['GET'])
        self.auth_bp.add_url_rule('/logout', view_func=self.logout, methods=['GET', 'POST'])


# Initialize and register AuthRoutes
AuthRoutes(auth_service, auth_bp)