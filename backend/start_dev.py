#!/usr/bin/env python3
"""
Development startup script for the Performance Analyzer Backend
Enables hot reload and better debugging for development
"""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def main():
    try:
        # Create Flask app
        app = create_app()
        
        # Import db after app creation
        from app import db
        
        # Initialize database tables
        print("Initializing database...")
        
        # Create SQLAlchemy tables
        with app.app_context():
            db.create_all()
            print("✅ SQLAlchemy tables created successfully!")
        
        # Initialize user tables and default data
        from app.models.user_models import UserManager
        user_manager = UserManager()
        print("✅ Database initialized successfully!")
        print("\n🔑 Default credentials:")
        print("   Admin: aman@gmail.com / aman123")
        print("   Teacher: aman@gmail.com / aman123")
        
        print("\n" + "="*60)
        print("🚀 STARTING FLASK DEVELOPMENT SERVER")
        print("="*60)
        print("📍 Server URL: http://localhost:5000")
        print("📍 API Base URL: http://localhost:5000/api/v1")
        print("🌐 CORS Enabled for:")
        print("   - http://localhost:3000 (React)")
        print("   - http://localhost:5173 (Vite)")
        print("   - http://127.0.0.1:3000")
        print("   - http://127.0.0.1:5173")
        print("🧪 Test CORS: http://localhost:5000/api/v1/cors/health")
        print("📊 Test Students API: http://localhost:5000/api/v1/students")
        print("="*60)
        print("🔄 Hot reload ENABLED for development")
        print("Press Ctrl+C to stop the server")
        print("="*60)
        
        # Run the app with development settings
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,  # Enable debug mode for development
            use_reloader=True,  # Enable auto-reload
            threaded=True
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main() 