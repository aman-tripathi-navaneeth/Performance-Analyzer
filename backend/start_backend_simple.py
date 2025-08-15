#!/usr/bin/env python3
"""
Simple backend server starter with error handling
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        print("🚀 Starting Flask Backend Server...")
        print("=" * 50)
        
        # Import and create app
        from app import create_app, db
        app = create_app()
        
        # Initialize database
        print("📊 Initializing database...")
        with app.app_context():
            db.create_all()
            print("✅ Database initialized successfully!")
        
        # Initialize user data
        try:
            from app.models.user_models import UserManager
            user_manager = UserManager()
            print("✅ User data initialized!")
        except Exception as user_error:
            print(f"⚠️  User initialization warning: {user_error}")
        
        print("\n" + "=" * 50)
        print("🌐 SERVER INFORMATION")
        print("=" * 50)
        print("📍 Backend URL: http://localhost:5000")
        print("📍 API Base URL: http://localhost:5000/api/v1")
        print("🧪 Health Check: http://localhost:5000/api/v1/cors/health")
        print("📤 Upload Endpoint: http://localhost:5000/api/v1/upload/subject")
        print("👥 Students API: http://localhost:5000/api/v1/students")
        print("=" * 50)
        print("✅ CORS enabled for React frontend (port 3000)")
        print("🔄 Server will auto-reload on code changes")
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start the server
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Try installing dependencies: pip install flask flask-sqlalchemy flask-cors pandas openpyxl python-dotenv")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()