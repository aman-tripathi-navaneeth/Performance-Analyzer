#!/usr/bin/env python3
"""
Simple server starter that bypasses database initialization issues
"""

import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_simple_app():
    """Create Flask app with minimal configuration"""
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple_performance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure CORS
    CORS(app, 
         origins=[
             "http://localhost:3000",
             "http://localhost:3001", 
             "http://localhost:3002",
             "http://localhost:5173",
             "http://127.0.0.1:3000",
             "http://127.0.0.1:3001",
             "http://127.0.0.1:3002",
             "http://127.0.0.1:5173"
         ],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"],
         supports_credentials=True
    )
    
    # Initialize database
    db = SQLAlchemy(app)
    
    # Import and register blueprints
    try:
        from app.api.auth import auth_bp
        from app.api.students import students_bp
        from app.api.analytics import analytics_bp
        from app.api.uploads import uploads_bp
        from app.api.sis_checker import sis_checker_bp
        from app.api.teacher_management import teacher_mgmt_bp
        from app.api.cors_test import cors_test_bp
        
        app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
        app.register_blueprint(students_bp, url_prefix='/api/v1/students')
        app.register_blueprint(analytics_bp, url_prefix='/api/v1')
        app.register_blueprint(uploads_bp, url_prefix='/api/v1/upload')
        app.register_blueprint(sis_checker_bp, url_prefix='/api/v1/sis')
        app.register_blueprint(teacher_mgmt_bp, url_prefix='/api/v1/admin')
        app.register_blueprint(cors_test_bp, url_prefix='/api/v1/cors')
        
        print("✅ All blueprints registered successfully")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not register some blueprints: {e}")
    
    # Create tables if they don't exist
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created")
        except Exception as e:
            print(f"⚠️  Warning: Database setup issue: {e}")
    
    return app

if __name__ == '__main__':
    print("🚀 Starting Simple Flask Server")
    print("=" * 50)
    
    app = create_simple_app()
    
    print("📍 Server URL: http://localhost:5000")
    print("📍 API Base URL: http://localhost:5000/api/v1")
    print("🌐 CORS enabled for ports 3000, 3001, 3002, 5173")
    print("=" * 50)
    
    # Start the server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Disable reloader to avoid database issues
    )