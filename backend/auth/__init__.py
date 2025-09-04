"""
LoginAuth Package
Provides authentication functionality for the EasyLesson application.
"""

from .AuthRoutes import auth_bp
from .decorators import login_required
from .AuthConfig import AuthConfig
from .AuthService import AuthService

__all__ = [
    'auth_bp',           # OAuth routes blueprint
    'login_required',    # Authentication decorator
    'AuthConfig',        # Configuration class
    'AuthService'        # Authentication service class
]