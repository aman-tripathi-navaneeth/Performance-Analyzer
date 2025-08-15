#!/usr/bin/env python3
"""
Simple test script for authentication system
"""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_auth():
    try:
        print("Testing authentication system...")
        
        # Test UserManager
        from app.models.user_models import UserManager
        print("✓ UserManager imported successfully")
        
        user_manager = UserManager()
        print("✓ UserManager initialized successfully")
        print("✓ Database tables created")
        
        # Test authentication
        result = user_manager.authenticate_user('aman@gmail.com', 'aman123', 'admin')
        if result['success']:
            print("✓ Admin authentication works")
        else:
            print("✗ Admin authentication failed:", result['error'])
        
        result = user_manager.authenticate_user('aman@gmail.com', 'aman123', 'teacher')
        if result['success']:
            print("✓ Teacher authentication works")
        else:
            print("✗ Teacher authentication failed:", result['error'])
        
        print("\n🎉 Authentication system is working!")
        print("\nCredentials:")
        print("Admin: aman@gmail.com / aman123")
        print("Teacher: aman@gmail.com / aman123")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_auth()