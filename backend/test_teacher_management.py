#!/usr/bin/env python3
"""
Test the teacher management system
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.user_models import UserManager

def test_teacher_management():
    """Test teacher management functionality"""
    app = create_app()
    
    with app.app_context():
        print("=== TESTING TEACHER MANAGEMENT SYSTEM ===")
        
        user_manager = UserManager()
        
        # Test 1: Get all teachers
        print("\n1. Testing get all teachers...")
        teachers = user_manager.get_all_teachers()
        print(f"   Found {len(teachers)} teachers:")
        for teacher in teachers:
            print(f"   - {teacher['name']} ({teacher['email']}) - {teacher['role']} - Active: {teacher['is_active']}")
        
        # Test 2: Add a new teacher
        print("\n2. Testing add new teacher...")
        result = user_manager.add_teacher(
            email="john.doe@college.edu",
            password="teacher123",
            name="John Doe"
        )
        
        if result['success']:
            print(f"   ✅ Successfully added teacher: {result['teacher']['name']}")
        else:
            print(f"   ❌ Failed to add teacher: {result['error']}")
        
        # Test 3: Try to add duplicate teacher
        print("\n3. Testing duplicate teacher prevention...")
        result = user_manager.add_teacher(
            email="john.doe@college.edu",
            password="teacher456",
            name="John Doe Duplicate"
        )
        
        if not result['success']:
            print(f"   ✅ Correctly prevented duplicate: {result['error']}")
        else:
            print(f"   ❌ Should have prevented duplicate!")
        
        # Test 4: Get all sections
        print("\n4. Testing get all sections...")
        sections = user_manager.get_all_sections()
        print(f"   Found {len(sections)} sections:")
        for section in sections:
            print(f"   - {section['name']} (Created: {section['created_at']})")
        
        # Test 5: Add a new section
        print("\n5. Testing add new section...")
        result = user_manager.add_section("CSE C")
        
        if result['success']:
            print(f"   ✅ Successfully added section: {result['section']['name']}")
        else:
            print(f"   ❌ Failed to add section: {result['error']}")
        
        # Test 6: Try to add duplicate section
        print("\n6. Testing duplicate section prevention...")
        result = user_manager.add_section("CSE C")
        
        if not result['success']:
            print(f"   ✅ Correctly prevented duplicate: {result['error']}")
        else:
            print(f"   ❌ Should have prevented duplicate!")
        
        # Test 7: Authentication test
        print("\n7. Testing teacher authentication...")
        auth_result = user_manager.authenticate_user(
            email="john.doe@college.edu",
            password="teacher123",
            role="teacher"
        )
        
        if auth_result['success']:
            print(f"   ✅ Teacher authentication successful: {auth_result['user']['name']}")
            print(f"   Token: {auth_result['token'][:20]}...")
        else:
            print(f"   ❌ Teacher authentication failed: {auth_result['error']}")
        
        # Test 8: Admin authentication test
        print("\n8. Testing admin authentication...")
        admin_auth = user_manager.authenticate_user(
            email="aman@gmail.com",
            password="aman123",
            role="admin"
        )
        
        if admin_auth['success']:
            print(f"   ✅ Admin authentication successful: {admin_auth['user']['name']}")
        else:
            print(f"   ❌ Admin authentication failed: {admin_auth['error']}")
        
        print("\n=== TEACHER MANAGEMENT TEST COMPLETED ===")
        
        # Final summary
        final_teachers = user_manager.get_all_teachers()
        final_sections = user_manager.get_all_sections()
        
        print(f"\n📊 FINAL SUMMARY:")
        print(f"   Total Teachers: {len(final_teachers)}")
        print(f"   Total Sections: {len(final_sections)}")
        print(f"   Active Teachers: {len([t for t in final_teachers if t['is_active']])}")
        print(f"   Inactive Teachers: {len([t for t in final_teachers if not t['is_active']])}")

if __name__ == "__main__":
    test_teacher_management()