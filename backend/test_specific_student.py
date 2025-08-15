#!/usr/bin/env python3
"""
Test script for specific student roll number 226K1A0546
"""

import requests
import json
import sys

def test_specific_student():
    """Test the SIS integration with the specific roll number"""
    
    roll_number = "226K1A0546"
    password = "226K1A0546"  # Same as roll number
    
    print(f"🧪 Testing SIS Integration for Student: {roll_number}")
    print("=" * 60)
    
    # Test API endpoint
    api_url = "http://localhost:5000/api/v1/sis/check-backlogs"
    
    payload = {
        "roll_number": roll_number,
        "password": password
    }
    
    try:
        print(f"📡 Making API request to: {api_url}")
        print(f"📋 Payload: {json.dumps(payload, indent=2)}")
        print()
        
        response = requests.post(api_url, json=payload, timeout=30)
        
        print(f"📊 Response Status: {response.status_code} {response.reason}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Request Successful!")
            print(f"📋 Response Data:")
            print(json.dumps(data, indent=2))
            
            if data.get('success'):
                result = data.get('data', {})
                print()
                print("🎯 Backlog Analysis Results:")
                print(f"   Roll Number: {result.get('roll_number')}")
                print(f"   Total Subjects: {result.get('total_subjects')}")
                print(f"   Passed Subjects: {result.get('passed_subjects')}")
                print(f"   Backlog Count: {result.get('backlog_count')}")
                print(f"   Overall Status: {result.get('overall_status')}")
                
                if result.get('backlogs'):
                    print()
                    print("📚 Backlog Details:")
                    for i, backlog in enumerate(result.get('backlogs', []), 1):
                        print(f"   {i}. {backlog.get('subject_name')} ({backlog.get('subject_code')})")
                        print(f"      Semester: {backlog.get('semester')}")
                        print(f"      Marks: {backlog.get('marks')}")
                        print(f"      Grade: {backlog.get('grade')}")
                        print()
                
                if result.get('backlog_count', 0) == 0:
                    print("🎉 No backlogs found! Student is clear.")
                else:
                    print(f"⚠️  {result.get('backlog_count')} backlog(s) found.")
                    
            else:
                print(f"❌ API returned error: {data.get('error')}")
                
        else:
            print(f"❌ API Request Failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error Details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Backend server is not running")
        print("💡 Start the backend server with: python run.py")
        
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
        
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        
    print()
    print("=" * 60)

def test_connection():
    """Test connection to SIS portal"""
    
    print("🔗 Testing SIS Portal Connection...")
    
    try:
        response = requests.get("http://localhost:5000/api/v1/sis/test-connection", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Connection test successful!")
            print(f"📋 Connection Details:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ Connection test failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection test error: {str(e)}")

if __name__ == "__main__":
    print("🎓 SIS Integration Test for Specific Student")
    print("=" * 60)
    
    # Test connection first
    test_connection()
    print()
    
    # Test specific student
    test_specific_student()
    
    print("🏁 Test completed!")