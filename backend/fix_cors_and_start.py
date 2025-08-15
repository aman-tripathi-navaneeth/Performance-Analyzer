#!/usr/bin/env python3
"""
Fix CORS and start server
"""
import sys
import os
import threading
import time
import requests

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_cors_after_startup():
    """Test CORS after server starts"""
    time.sleep(3)  # Wait for server to start
    
    print("\n" + "="*50)
    print("🧪 TESTING CORS CONFIGURATION")
    print("="*50)
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:5000/api/v1/cors/health")
        if response.status_code == 200:
            print("✅ Health check: PASSED")
        else:
            print(f"❌ Health check: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Health check: ERROR - {e}")
    
    try:
        # Test CORS with Origin header
        headers = {'Origin': 'http://localhost:3000'}
        response = requests.get("http://localhost:5000/api/v1/cors/test", headers=headers)
        if response.status_code == 200:
            cors_header = response.headers.get('Access-Control-Allow-Origin')
            if cors_header:
                print("✅ CORS test: PASSED")
                print(f"   Access-Control-Allow-Origin: {cors_header}")
            else:
                print("❌ CORS test: No CORS headers found")
        else:
            print(f"❌ CORS test: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ CORS test: ERROR - {e}")
    
    try:
        # Test students endpoint
        headers = {'Origin': 'http://localhost:3000'}
        response = requests.get("http://localhost:5000/api/v1/students", headers=headers)
        if response.status_code == 200:
            print("✅ Students API: PASSED")
        else:
            print(f"❌ Students API: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Students API: ERROR - {e}")
    
    print("="*50)
    print("🎯 If all tests passed, CORS is working correctly!")
    print("🌐 Your React app should now be able to connect to the API")
    print("="*50)

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
            print("SQLAlchemy tables created successfully!")
        
        # Initialize user tables and default data
        from app.models.user_models import UserManager
        user_manager = UserManager()
        print("Database initialized successfully!")
        
        print("\n" + "="*60)
        print("🚀 STARTING FLASK SERVER WITH ENHANCED CORS")
        print("="*60)
        print("📍 Server URL: http://localhost:5000")
        print("📍 API Base URL: http://localhost:5000/api/v1")
        print("🌐 CORS Enabled for:")
        print("   ✅ http://localhost:3000 (React)")
        print("   ✅ http://localhost:5173 (Vite)")
        print("   ✅ http://127.0.0.1:3000")
        print("   ✅ http://127.0.0.1:5173")
        print("   ✅ http://localhost:3001")
        print("🧪 Test endpoints:")
        print("   - http://localhost:5000/api/v1/cors/health")
        print("   - http://localhost:5000/api/v1/students")
        print("="*60)
        print("Press Ctrl+C to stop the server")
        print("="*60)
        
        # Start CORS test in background
        test_thread = threading.Thread(target=test_cors_after_startup)
        test_thread.daemon = True
        test_thread.start()
        
        # Run the app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False  # Disable reloader to prevent threading issues
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()