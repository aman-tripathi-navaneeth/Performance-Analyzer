#!/usr/bin/env python3
import urllib.request
import json

def test_class_api():
    try:
        url = "http://localhost:5000/api/v1/class/performance/1/CSEA"
        print(f"Testing URL: {url}")
        
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            print(f"Status Code: {response.status}")
            print("Response:")
            print(json.dumps(data, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_class_api()