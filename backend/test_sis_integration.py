#!/usr/bin/env python3
"""
Test SIS Integration directly without Flask app
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.sis_integration import MockSISIntegration
import json

def test_sis_integration():
    """Test the SIS integration service"""
    print("🧪 Testing SIS Integration Service")
    print("=" * 50)
    
    # Initialize mock SIS service
    sis_service = MockSISIntegration()
    
    # Test cases
    test_cases = [
        "226K1A0546",  # Special case with backlogs
        "226K1A0547",  # Random student
        "226K1A0548",  # Another random student
    ]
    
    for roll_number in test_cases:
        print(f"\n📋 Testing roll number: {roll_number}")
        print("-" * 30)
        
        try:
            result = sis_service.check_student_backlogs(roll_number)
            
            print(f"✅ Success: {result['success']}")
            print(f"📊 Total Subjects: {result['total_subjects']}")
            print(f"✅ Passed: {result['passed_subjects']}")
            print(f"❌ Backlogs: {result['backlog_count']}")
            print(f"📈 Status: {result['overall_status']}")
            
            if result['backlogs']:
                print(f"\n📋 Backlog Details:")
                for i, backlog in enumerate(result['backlogs'], 1):
                    print(f"  {i}. {backlog['subject_name']} ({backlog['subject_code']})")
                    print(f"     Semester: {backlog['semester']}, Marks: {backlog['marks']}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n🎯 Testing complete!")

if __name__ == "__main__":
    test_sis_integration()