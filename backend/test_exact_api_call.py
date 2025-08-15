#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_exact_api_call():
    """Test the exact API call that should work for 2nd Year CSE A"""
    print("=== TESTING EXACT API CALL FOR 2ND YEAR CSE A ===")
    
    app = create_app()
    
    with app.test_client() as client:
        # Test the exact call that frontend should make
        print("🧪 Testing: GET /api/v1/class/performance/2/CSE A")
        
        # Test with URL encoding (how frontend sends it)
        encoded_section = "CSE%20A"
        response = client.get(f'/api/v1/class/performance/2/{encoded_section}')
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"Response Success: {data.get('success')}")
            
            if data.get('success'):
                class_data = data['data']
                print(f"✅ SUCCESS: {class_data['class_name']}")
                print(f"   Students: {class_data['overall_stats']['total_students']}")
                print(f"   Subjects: {class_data['overall_stats']['total_subjects']}")
                print(f"   Average: {class_data['overall_stats']['overall_average']}%")
                print(f"   Grade: {class_data['overall_stats']['grade']}")
                
                print(f"\n📚 Subjects ({len(class_data['subjects_performance'])}):")
                for subject in class_data['subjects_performance']:
                    print(f"   - {subject['base_subject_name']}: {subject['class_average']}%")
                
                print(f"\n👥 Students ({len(class_data['students_list'])}):")
                for i, student in enumerate(class_data['students_list'][:5]):  # Show first 5
                    print(f"   {i+1}. {student['full_name']}: {student['average_percentage']}%")
                
                if len(class_data['students_list']) > 5:
                    print(f"   ... and {len(class_data['students_list']) - 5} more students")
                    
            else:
                print(f"❌ API Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.get_data(as_text=True)}")
        
        # Also test without encoding to compare
        print("\n🧪 Testing: GET /api/v1/class/performance/2/CSE A (without encoding)")
        response2 = client.get('/api/v1/class/performance/2/CSE A')
        print(f"Status Code: {response2.status_code}")
        
        if response2.status_code == 200:
            data2 = response2.get_json()
            if data2.get('success'):
                print(f"✅ Also works without encoding: {data2['data']['overall_stats']['total_students']} students")
            else:
                print(f"❌ Error without encoding: {data2.get('error')}")

if __name__ == "__main__":
    test_exact_api_call()