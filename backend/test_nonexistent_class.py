#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_nonexistent_class():
    """Test what happens when we request a class that doesn't exist"""
    print("=== TESTING NON-EXISTENT CLASS PERFORMANCE ===")
    
    app = create_app()
    
    with app.test_client() as client:
        # Test cases that should fail
        test_cases = [
            (1, "CSE A"),  # 1st Year CSE A doesn't exist
            (3, "CSE A"),  # 3rd Year CSE A doesn't exist
            (2, "CSE B"),  # 2nd Year CSE B doesn't exist
        ]
        
        for year, section in test_cases:
            print(f"\n🧪 Testing Year {year}, Section {section} (should not exist)...")
            
            response = client.get(f'/api/v1/class/performance/{year}/{section}')
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    class_data = data['data']
                    print(f"✅ API returned success: {class_data['class_name']}")
                    print(f"   Students: {class_data['overall_stats']['total_students']}")
                    print(f"   Subjects: {class_data['overall_stats']['total_subjects']}")
                    print(f"   Average: {class_data['overall_stats']['overall_average']}%")
                    
                    if class_data['overall_stats']['total_students'] == 0:
                        print("   ⚠️ This class has 0 students - should show 'no data' message")
                    else:
                        print("   ✅ This class has students")
                else:
                    print(f"❌ API Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"   Response: {response.get_data(as_text=True)}")

if __name__ == "__main__":
    test_nonexistent_class()