"""
EasyLesson Web Application - Home Module
Main application factory and route definitions for the home page functionality.
"""

import os
from flask import Flask, render_template, session, jsonify
from loginauth import auth_bp, login_required, AuthConfig


class HomeConfig:
    """Configuration specific to the home application"""
    
    # Server settings
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Template and static folders
    TEMPLATE_FOLDER = '../frontend/templates'
    STATIC_FOLDER = '../frontend/static'
    
    # Application info
    APP_NAME = 'EasyLesson'
    VERSION = '1.0.0'


class HomeRoutes:
    """Route handlers for the home application"""
    
    @staticmethod
    def index():
        """Home page route"""
        return render_template('index.html')
    
    @staticmethod
    @login_required
    def dashboard():
        """Protected dashboard page - only accessible after login"""
        user = session.get('user')
        if not user:
            # This shouldn't happen with @login_required, but safety check
            return jsonify({'error': 'User session not found'}), 401
        
        return render_template('dashboard.html', user=user)
    
    @staticmethod
    def health():
        """Health check endpoint for monitoring"""
        return {
            'status': 'healthy',
            'service': f'{HomeConfig.APP_NAME} API',
            'version': HomeConfig.VERSION
        }, 200


def create_app():
    """
    Application factory pattern for creating Flask app instances.
    This makes it easier to configure different environments and testing.
    """
    app = Flask(__name__, 
                template_folder=HomeConfig.TEMPLATE_FOLDER,
                static_folder=HomeConfig.STATIC_FOLDER)
    
    # Load configuration from AuthConfig
    app.config.from_object(AuthConfig)
    
    # Register authentication blueprint
    app.register_blueprint(auth_bp)
    
    # Register home routes
    _register_home_routes(app)
    
    return app


def _register_home_routes(app):
    """Register home-specific routes to the Flask app"""
    app.add_url_rule('/', 'index', HomeRoutes.index)
    app.add_url_rule('/dashboard', 'dashboard', HomeRoutes.dashboard)
    app.add_url_rule('/health', 'health', HomeRoutes.health)


def validate_environment():
    """Validate that required environment variables are set"""
    missing_vars = []
    
    if not AuthConfig.GOOGLE_CLIENT_ID:
        missing_vars.append('GOOGLE_CLIENT_ID')
    
    if not AuthConfig.GOOGLE_CLIENT_SECRET:
        missing_vars.append('GOOGLE_CLIENT_SECRET')
    
    return missing_vars


def print_startup_info():
    """Print helpful startup information"""
    print("🚀 Starting EasyLesson server...")
    print(f"📝 Access your app at: http://localhost:{HomeConfig.PORT}")
    print(f"🔐 Dashboard at: http://localhost:{HomeConfig.PORT}/dashboard (requires login)")
    print(f"❤️  Health check at: http://localhost:{HomeConfig.PORT}/health")


def main():
    """Main application entry point"""
    # Validate environment
    missing_vars = validate_environment()
    if missing_vars:
        print("⚠️  Warning: Missing required environment variables!")
        print(f"Please set: {', '.join(missing_vars)}")
        print("Check your .env file or environment configuration.")
        print("The app may not work correctly without these variables.\n")
    
    # Create and run the app
    app = create_app()
    print_startup_info()
    
    app.run(
        debug=True,
        host=HomeConfig.HOST,
        port=HomeConfig.PORT
    )


# Entry point
if __name__ == '__main__':
    main()