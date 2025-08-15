#!/usr/bin/env python3
"""
Test CORS configuration
"""
import requests
import json

def test_cors():
    """Test CORS configuration"""
    base_url = "http://localhost:5000/api/v1"
    
    print("=== TESTING CORS CONFIGURATION ===")
    
    # Test 1: Health check
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/cors/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   CORS Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: CORS test endpoint
    print("\n2. Testing CORS test endpoint...")
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{base_url}/cors/test", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   CORS Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: OPTIONS preflight request
    print("\n3. Testing OPTIONS preflight request...")
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{base_url}/cors/test", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Students endpoint
    print("\n4. Testing students endpoint...")
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{base_url}/students", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Students found: {len(data.get('data', {}).get('students', []))}")
        print(f"   CORS Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== CORS TEST COMPLETED ===")

if __name__ == "__main__":
    test_cors()