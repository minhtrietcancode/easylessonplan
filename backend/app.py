import os
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from loginauth import auth_bp, login_required, Config

def create_app():
    """Application factory pattern"""
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize session
    Session(app)
    
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
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - EasyLesson</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: #f8f9fc; 
                margin: 0; 
                padding: 20px;
            }}
            .dashboard {{ 
                max-width: 800px; 
                margin: 0 auto; 
                background: white; 
                padding: 40px; 
                border-radius: 10px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .user-info {{ 
                text-align: center; 
                margin-bottom: 30px;
            }}
            .user-info img {{ 
                border-radius: 50%; 
                width: 80px; 
                height: 80px;
                margin-bottom: 15px;
            }}
            .btn {{ 
                background: #4C50CC; 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px;
                display: inline-block;
                margin: 10px;
            }}
            .btn:hover {{ background: #4247B0; }}
        </style>
    </head>
    <body>
        <div class="dashboard">
            <div class="user-info">
                <img src="{user.get('picture', '')}" alt="Profile Picture">
                <h2>Welcome, {user.get('name', 'User')}!</h2>
                <p>Email: {user.get('email', '')}</p>
            </div>
            <div style="text-align: center;">
                <h3>Your EasyLesson Dashboard</h3>
                <p>Start creating amazing lesson plans with AI assistance!</p>
                <a href="/auth/logout" class="btn">Logout</a>
                <a href="/" class="btn">Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """

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