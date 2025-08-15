#!/usr/bin/env python3
import urllib.request
import json

def test_cse_a():
    try:
        # Test the exact case that was failing
        url = "http://localhost:5000/api/v1/class/performance/2/CSE%20A"
        print(f"Testing URL: {url}")
        
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            print(f"Status Code: {response.status}")
            print(f"Success: {data.get('success')}")
            
            if data.get('success') and 'data' in data:
                class_data = data['data']
                stats = class_data.get('overall_stats', {})
                print(f"Students: {stats.get('total_students', 0)}")
                print(f"Subjects: {stats.get('total_subjects', 0)}")
                print(f"Average: {stats.get('overall_average', 0)}%")
                
                # This is what the frontend checks
                should_show_data = data['success'] and class_data and stats.get('total_students', 0) > 0
                print(f"Frontend should show data: {should_show_data}")
            else:
                print("No data or unsuccessful response")
                
            print("\nFull Response:")
            print(json.dumps(data, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_cse_a()