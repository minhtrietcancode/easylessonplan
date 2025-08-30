import json
import requests
import os
from flask import Blueprint, request, redirect, session, url_for, jsonify
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.exceptions
from .config import Config

# Set OAUTHLIB_INSECURE_TRANSPORT based on Config
# This allows insecure transport for development (HTTP instead of HTTPS)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' if Config.OAUTHLIB_INSECURE_TRANSPORT else '0'

# Create Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


class AuthService:
    """Handles Google OAuth authentication and user session management."""

    @staticmethod
    def create_flow():
        """Create and configure the OAuth flow."""
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": Config.GOOGLE_CLIENT_ID,
                    "client_secret": Config.GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost:5000/auth/callback"]
                }
            },
            scopes=["https://www.googleapis.com/auth/userinfo.profile", "openid", "https://www.googleapis.com/auth/userinfo.email"]
        )
        flow.redirect_uri = "http://localhost:5000/auth/callback"
        return flow

def login_required(f):
    """Decorator to require login for certain routes"""
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


class AuthRoutes:
    """Handles authentication-related routes."""

    @staticmethod
    def login():
        """Initiate Google OAuth login"""
        try:
            flow = AuthService.create_flow()
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            session['state'] = state
            return redirect(authorization_url)
        except Exception as e:
            return jsonify({'error': f'Login failed: {str(e)}'}), 500

    @staticmethod
    def callback():
        """Handle Google OAuth callback"""
        try:
            # Verify state parameter
            if request.args.get('state') != session.get('state'):
                return jsonify({'error': 'Invalid state parameter'}), 400

            flow = AuthService.create_flow()

            # Fetch token using authorization code
            flow.fetch_token(authorization_response=request.url)

            # Get user info from Google
            credentials = flow.credentials
            request_session = google_requests.Request()

            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                credentials.id_token, request_session, Config.GOOGLE_CLIENT_ID
            )

            # Store user info in session
            session['user'] = {
                'id': idinfo['sub'],
                'name': idinfo['name'],
                'email': idinfo['email'],
                'picture': idinfo.get('picture', '')
            }

            # Redirect to dashboard or home page
            return redirect(url_for('dashboard'))

        except google.auth.exceptions.GoogleAuthError as e:
            return jsonify({'error': f'Google authentication error: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error': f'Callback failed: {str(e)}'}), 500

    @staticmethod
    def logout():
        """Logout user by clearing session"""
        session.clear()
        return redirect(url_for('index'))

    @staticmethod
    def get_user():
        """Get current user information"""
        if 'user' not in session:
            return jsonify({'user': None}), 200
        return jsonify({'user': session['user']}), 200

# Register routes from AuthRoutes class
auth_bp.add_url_rule('/login', view_func=AuthRoutes.login)
auth_bp.add_url_rule('/callback', view_func=AuthRoutes.callback)
auth_bp.add_url_rule('/logout', view_func=AuthRoutes.logout)
auth_bp.add_url_rule('/user', view_func=AuthRoutes.get_user)