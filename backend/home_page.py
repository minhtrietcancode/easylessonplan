import os
from flask import Flask, render_template, session, redirect, url_for
from loginauth import auth_bp, login_required, Config

def create_app():
    """Application factory pattern"""
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Load configuration
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    
    return app

app = create_app()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Protected dashboard page - only accessible after login"""
    user = session.get('user')
    return render_template('dashboard.html', user=user)

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'EasyLesson API'}, 200

if __name__ == '__main__':
    # Check if required environment variables are set
    if not Config.GOOGLE_CLIENT_ID or not Config.GOOGLE_CLIENT_SECRET:
        print("⚠️  Warning: Google OAuth credentials not found!")
        print("Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables.")
        print("See setup instructions below.")
    
    print("🚀 Starting EasyLesson server...")
    print("📝 Access your app at: http://localhost:5000")
    print("🔐 Dashboard at: http://localhost:5000/dashboard (requires login)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)