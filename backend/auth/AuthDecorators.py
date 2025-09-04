"""
Authentication Decorators Module
Provides decorators for route protection and authentication checks.
"""

import functools
from flask import session, redirect, url_for


def login_required(f):
    """
    Decorator to require login for certain routes.
    Redirects to login page if user is not authenticated.
    
    Usage:
        @login_required
        def protected_route():
            return "This requires login"
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function