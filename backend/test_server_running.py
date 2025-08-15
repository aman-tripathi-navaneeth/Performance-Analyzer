#!/usr/bin/env python3
"""
Test if the server is running and accessible
"""
import urllib.request
import json

def test_server():
    print("🧪 Testing Backend Server...")
    print("=" * 40)
    
    # Test health endpoint
    try:
        with urllib.request.urlopen('http://localhost:5000/api/v1/cors/health') as response:
            data = json.loads(response.read().decode())
            if data.get('success'):
                print("✅ Health check: PASSED")
                print(f"   Message: {data.get('message')}")
            else:
                print("❌ Health check: FAILED")
    except Exception as e:
        print(f"❌ Health check: ERROR - {e}")
        return False
    
    # Test upload endpoint (OPTIONS request)
    try:
        req = urllib.request.Request('http://localhost:5000/api/v1/upload/subject')
        req.get_method = lambda: 'OPTIONS'
        req.add_header('Origin', 'http://localhost:3000')
        req.add_header('Access-Control-Request-Method', 'POST')
        
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("✅ Upload endpoint: ACCESSIBLE")
            else:
                print(f"⚠️  Upload endpoint: Status {response.status}")
    except Exception as e:
        print(f"❌ Upload endpoint: ERROR - {e}")
    
    # Test students endpoint
    try:
        with urllib.request.urlopen('http://localhost:5000/api/v1/students') as response:
            data = json.loads(response.read().decode())
            if data.get('success'):
                student_count = len(data.get('data', {}).get('students', []))
                print(f"✅ Students API: PASSED ({student_count} students found)")
            else:
                print("❌ Students API: FAILED")
    except Exception as e:
        print(f"❌ Students API: ERROR - {e}")
    
    print("=" * 40)
    print("🎯 If all tests passed, your backend is ready!")
    print("🌐 You can now upload files from your React app")
    return True

if __name__ == "__main__":
    test_server()