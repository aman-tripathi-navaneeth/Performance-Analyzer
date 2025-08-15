#!/usr/bin/env python3
"""
Simple server starter that avoids Flask auto-reload database issues
"""

import os
import sys
from flask import Flask
from app import create_app, db

def main():
    """Start the Flask server without auto-reload to avoid database lock issues"""
    
    print("🚀 Starting Performance Analyzer Backend Server")
    print("=" * 50)
    
    try:
        # Create Flask app
        app = create_app()
        
        # Create database tables within app context
        with app.app_context():
            print("📊 Initializing database...")
            db.create_all()
            print("✅ Database initialized successfully!")
            
            # Create default users if they don't exist
            from app.models.user_models import User
            
            admin_exists = User.query.filter_by(email='aman@gmail.com').first()
            if not admin_exists:
                admin_user = User(
                    email='aman@gmail.com',
                    role='admin'
                )
                admin_user.set_password('aman123')
                db.session.add(admin_user)
                
                teacher_user = User(
                    email='teacher@gmail.com', 
                    role='teacher'
                )
                teacher_user.set_password('teacher123')
                db.session.add(teacher_user)
                
                db.session.commit()
                print("👤 Default users created!")
            else:
                print("👤 Default users already exist")
        
        print("\n" + "=" * 50)
        print("🌟 SERVER READY!")
        print("=" * 50)
        print("📍 Server URL: http://localhost:5000")
        print("📍 API Base URL: http://localhost:5000/api/v1")
        print("🧪 Test SIS API: http://localhost:5000/api/v1/sis/test-connection")
        print("📊 Test Students API: http://localhost:5000/api/v1/students")
        print("\n🔑 Default Login Credentials:")
        print("   Admin: aman@gmail.com / aman123")
        print("   Teacher: teacher@gmail.com / teacher123")
        print("=" * 50)
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start server without auto-reload
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # Disable debug mode to avoid auto-reload
            use_reloader=False,  # Explicitly disable reloader
            threaded=True
        )
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()