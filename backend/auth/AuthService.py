# File: backend\auth\AuthService.py
"""
Authentication Service Module
Pure authentication service logic with no Flask dependencies.
"""

import os
from typing import Dict, Optional
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.exceptions


class AuthService:
    """Pure authentication service - no Flask dependencies"""
    
    def __init__(self, config):
        """Initialize auth service with configuration"""
        self.config = config
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' if config.OAUTHLIB_INSECURE_TRANSPORT else '0'
    
    def create_oauth_flow(self) -> Flow:
        """Create and configure the Google OAuth flow"""
        client_config = {
            "web": {
                "client_id": self.config.GOOGLE_CLIENT_ID,
                "client_secret": self.config.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [self.config.get_redirect_uri()]
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
        
        flow.redirect_uri = self.config.get_redirect_uri()
        return flow
    
    def verify_token_and_get_user(self, credentials) -> Dict:
        """Verify OAuth token and extract user information"""
        request_session = google_requests.Request()
        
        idinfo = id_token.verify_oauth2_token(
            credentials.id_token, 
            request_session, 
            self.config.GOOGLE_CLIENT_ID
        )
        
        return {
            'id': idinfo['sub'],
            'name': idinfo['name'],
            'email': idinfo['email'],
            'picture': idinfo.get('picture', ''),
            'verified_email': idinfo.get('email_verified', False)
        }
    
    @staticmethod
    def get_current_user(session) -> Optional[Dict]:
        """Get current user from session"""
        return session.get('user')
    
    @staticmethod
    def store_user_in_session(session, user_info: Dict):
        """Store user information in session"""
        session['user'] = user_info
        session.permanent = True
    
    @staticmethod
    def clear_session(session):
        """Clear user session"""
        session.clear()