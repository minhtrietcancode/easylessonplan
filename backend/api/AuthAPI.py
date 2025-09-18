# File: backend/api/AuthAPI.py
"""
Authentication API Module
Contains all authentication route methods including OAuth flow and user info endpoints.
This file only contains methods - routes are registered in backend/APIRoutes.py
"""

from flask import request, redirect, session, url_for, jsonify, current_app
from .BaseAPI import BaseAPI
import google.auth.exceptions
import sys
import os

from backend.service.auth.AuthService import AuthService
from backend.service.auth.AuthConfig import AuthConfig
from backend.service.database.DatabaseHandler import DatabaseHandler # Import DatabaseHandler

# Initialize auth service
auth_service = AuthService(AuthConfig)


class AuthAPI(BaseAPI):
    """API handler for all authentication operations"""

    @classmethod
    def login(cls):
        """
        GET /auth/login - Initiate Google OAuth login process
        Redirects user to Google OAuth page
        """
        try:
            flow = auth_service.create_oauth_flow()
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

    @classmethod
    def callback(cls):
        """
        GET /auth/callback - Handle Google OAuth callback
        Google redirects back to this endpoint after user authentication
        """
        db_handler = DatabaseHandler() # Initialize DatabaseHandler
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
            flow = auth_service.create_oauth_flow()
            flow.fetch_token(authorization_response=request.url)
            
            # Verify token and get user info
            user_info = auth_service.verify_token_and_get_user(flow.credentials)
            
            # Check if user exists in the database, if not, create them
            email = user_info.get('email')
            full_name = user_info.get('name') # Get the full name
            first_name = full_name.split(' ')[0] if full_name else None # Extract first name
            
            if email and first_name:
                user_exists = db_handler.check_exist_user(email, first_name)
                if not user_exists:
                    db_handler.insert_user(email, first_name)
                    current_app.logger.info(f"New user created in DB: {email}")
                else:
                    current_app.logger.info(f"User already exists in DB: {email}")
            else:
                current_app.logger.warning(f"Could not get email or first name from user_info: {user_info}")

            # Store user in session
            auth_service.store_user_in_session(session, user_info)
            
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
        finally:
            db_handler.close() # Close database connection

    @classmethod
    def logout(cls):
        """
        GET/POST /auth/logout - Logout user and redirect to home page
        Clears user session and redirects to home
        """
        user = auth_service.get_current_user(session)
        if user:
            current_app.logger.info(f"User logged out: {user.get('email', 'unknown')}")
        else:
            current_app.logger.info("Logout attempted with no active session")
        
        auth_service.clear_session(session)
        return redirect(url_for('index'))

    @classmethod
    def get_user_info(cls):
        """
        GET /auth/user - Get current user information from session
        
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