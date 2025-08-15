#!/usr/bin/env python3
import urllib.request
import json

def test_year1_csea():
    try:
        # Test the exact case that's failing
        url = "http://localhost:5000/api/v1/class/performance/1/CSEA"
        print(f"Testing URL: {url}")
        
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            print(f"Status Code: {response.status}")
            print(f"Response type: {type(data)}")
            print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            # Check if it has the success wrapper
            if 'success' in data:
                print(f"✅ Has 'success' field: {data['success']}")
                if 'data' in data:
                    print(f"✅ Has 'data' field with {len(data['data'])} keys")
                    class_data = data['data']
                    if 'overall_stats' in class_data:
                        stats = class_data['overall_stats']
                        print(f"✅ Students: {stats.get('total_students', 0)}")
                else:
                    print("❌ Missing 'data' field")
            else:
                print("❌ Missing 'success' field - this is the problem!")
                # Check if it looks like the data was returned directly
                if 'overall_stats' in data:
                    stats = data['overall_stats']
                    print(f"📊 Direct data - Students: {stats.get('total_students', 0)}")
                    print("🔧 This suggests the API is returning data directly instead of wrapped")
            
            print("\nFull Response:")
            print(json.dumps(data, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_year1_csea()