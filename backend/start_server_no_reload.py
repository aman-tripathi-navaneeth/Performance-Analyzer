#!/usr/bin/env python3
"""
Start Flask server without auto-reload to avoid database locking issues
"""

from app import create_app, db

def main():
    """Start the Flask server"""
    print("🚀 Starting Flask Backend Server (No Auto-Reload)")
    print("=" * 60)
    
    try:
        # Create Flask app
        app = create_app()
        
        with app.app_context():
            print("📊 Initializing database...")
            db.create_all()
            print("✅ Database initialized successfully!")
            
            # Initialize user data
            from app.models.user_models import UserManager
            user_manager = UserManager()
            print("✅ User data initialized!")
        
        print("\n" + "=" * 60)
        print("🌐 SERVER INFORMATION")
        print("=" * 60)
        print("📍 Backend URL: http://localhost:5000")
        print("📍 API Base URL: http://localhost:5000/api/v1")
        print("🧪 Health Check: http://localhost:5000/api/v1/cors/health")
        print("📤 Upload Endpoint: http://localhost:5000/api/v1/upload/subject")
        print("👥 Students API: http://localhost:5000/api/v1/students")
        print("📊 Dashboard API: http://localhost:5000/api/v1/class/overview")
        print("=" * 60)
        print("✅ CORS enabled for React frontend (port 3000)")
        print("⚠️  Auto-reload disabled to prevent database issues")
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Start server without debug mode to avoid reloader
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # Disable debug to avoid reloader
            use_reloader=False  # Explicitly disable reloader
        )
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()