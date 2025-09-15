"""
Authentication Configuration Module
Centralized configuration management for OAuth and application settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AuthConfig:
    """
    Authentication and application configuration settings.
    All configuration values are loaded from environment variables.
    """
    
    # Flask core settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Google OAuth 2.0 Configuration
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid_configuration"
    
    # OAuth 2.0 settings
    OAUTHLIB_INSECURE_TRANSPORT = os.environ.get('OAUTHLIB_INSECURE_TRANSPORT', '0') == '1'
    
    # Session settings
    SESSION_PERMANENT = True
    SESSION_TYPE = 'filesystem'  # Can be changed to 'redis' for production
    
    @classmethod
    def validate_config(cls):
        """
        Validate that all required configuration values are present.
        Returns a list of missing required variables.
        """
        required_vars = {
            'GOOGLE_CLIENT_ID': cls.GOOGLE_CLIENT_ID,
            'GOOGLE_CLIENT_SECRET': cls.GOOGLE_CLIENT_SECRET
        }
        
        missing = [var for var, value in required_vars.items() if not value]
        return missing
    
    @classmethod
    def is_development(cls):
        """Check if running in development mode"""
        return os.environ.get('FLASK_ENV', 'production').lower() == 'development'
    
    @classmethod
    def get_redirect_uri(cls, base_url=None):
        """Get the OAuth redirect URI, with optional base URL override"""
        if base_url:
            return f"{base_url}/auth/callback"
        return "http://localhost:5000/auth/callback"  # Default for development