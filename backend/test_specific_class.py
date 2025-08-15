#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_specific_class():
    """Test specific class performance that might be failing"""
    print("=== TESTING SPECIFIC CLASS PERFORMANCE ===")
    
    app = create_app()
    
    with app.test_client() as client:
        # Test the classes that should exist
        test_cases = [
            (2, "CSE A"),
            (2, "CSEA"), 
            (1, "CSEA")
        ]
        
        for year, section in test_cases:
            print(f"\n🧪 Testing Year {year}, Section {section}...")
            
            response = client.get(f'/api/v1/class/performance/{year}/{section}')
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    class_data = data['data']
                    print(f"✅ Success: {class_data['class_name']}")
                    print(f"   Students: {class_data['overall_stats']['total_students']}")
                    print(f"   Subjects: {class_data['overall_stats']['total_subjects']}")
                    print(f"   Average: {class_data['overall_stats']['overall_average']}%")
                else:
                    print(f"❌ API Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"   Response: {response.get_data(as_text=True)}")

if __name__ == "__main__":
    test_specific_class()