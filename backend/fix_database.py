#!/usr/bin/env python3
"""
Fix database issues and create a fresh database
"""

import os
import shutil
from app import create_app, db

def fix_database():
    """Fix database issues"""
    print("🔧 Fixing Database Issues")
    print("=" * 50)
    
    # Remove existing database files
    instance_dir = "instance"
    if os.path.exists(instance_dir):
        print(f"📁 Removing existing instance directory: {instance_dir}")
        try:
            shutil.rmtree(instance_dir)
            print("✅ Instance directory removed")
        except Exception as e:
            print(f"⚠️  Warning: Could not remove instance directory: {e}")
    
    # Create fresh instance directory
    os.makedirs(instance_dir, exist_ok=True)
    print(f"📁 Created fresh instance directory: {instance_dir}")
    
    # Create Flask app and database
    try:
        print("🚀 Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            print("📊 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Import and create default users
            from app.models.user_models import UserManager
            
            print("👤 Creating default users...")
            user_manager = UserManager()
            print("✅ Default users created!")
            
            print("🎉 Database setup completed successfully!")
            print("\nDefault credentials:")
            print("Email: aman@gmail.com")
            print("Password: aman123")
            
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = fix_database()
    if success:
        print("\n🚀 Database is ready! You can now start the server with:")
        print("python run.py")
    else:
        print("\n❌ Database setup failed!")