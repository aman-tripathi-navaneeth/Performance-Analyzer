#!/usr/bin/env python3

import requests
import json

def test_class_performance_api():
    """Test the class performance API response structure"""
    
    try:
        print("=== Testing Class Performance API ===")
        
        # Test the API endpoint
        url = 'http://localhost:5000/api/v1/class/performance/1/CSEA'
        print(f"Testing URL: {url}")
        
        response = requests.get(url)
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Success Field: {data.get('success')}")
        print(f"Has Data Field: {'data' in data}")
        
        if 'data' in data:
            class_data = data['data']
            stats = class_data.get('overall_stats', {})
            print(f"Students: {stats.get('total_students', 0)}")
            print(f"Subjects: {stats.get('total_subjects', 0)}")
            print(f"Class Name: {class_data.get('class_name', 'N/A')}")
            print(f"Students List Length: {len(class_data.get('students_list', []))}")
            print(f"Subjects Performance Length: {len(class_data.get('subjects_performance', []))}")
        
        print("\n=== Response Structure Check ===")
        expected_structure = {
            'success': bool,
            'data': {
                'year': int,
                'section': str,
                'class_name': str,
                'overall_stats': dict,
                'subjects_performance': list,
                'students_list': list
            }
        }
        
        # Check structure
        structure_ok = True
        if not isinstance(data.get('success'), bool):
            print("❌ Missing or invalid 'success' field")
            structure_ok = False
        
        if 'data' not in data:
            print("❌ Missing 'data' field")
            structure_ok = False
        else:
            class_data = data['data']
            required_fields = ['year', 'section', 'class_name', 'overall_stats', 'subjects_performance', 'students_list']
            for field in required_fields:
                if field not in class_data:
                    print(f"❌ Missing '{field}' in data")
                    structure_ok = False
        
        if structure_ok:
            print("✅ Response structure is correct")
        
        print("\n=== Frontend Logic Test ===")
        # Simulate frontend logic
        classData = data.get('success') and data.get('data')
        shouldShowNoData = not data.get('success') or not classData or classData.get('overall_stats', {}).get('total_students', 0) == 0
        
        print(f"Class Data Exists: {bool(classData)}")
        print(f"Should Show No Data: {shouldShowNoData}")
        print(f"Should Show Content: {not shouldShowNoData}")
        
        if not shouldShowNoData:
            print("✅ Frontend should display class performance content")
        else:
            print("❌ Frontend will show 'No Data Available'")
        
        print("\n=== Sample Data ===")
        if classData and classData.get('students_list'):
            print("First student:")
            print(json.dumps(classData['students_list'][0], indent=2))
        
        if classData and classData.get('subjects_performance'):
            print("First subject:")
            print(json.dumps(classData['subjects_performance'][0], indent=2))
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Backend is not running on port 5000")
        print("Please start the backend server first")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_class_performance_api()