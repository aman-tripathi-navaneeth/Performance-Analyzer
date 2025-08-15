#!/usr/bin/env python3
"""
Test the dashboard API endpoint directly
"""

import requests
import json

def test_dashboard_api():
    """Test the dashboard API endpoint"""
    print("🧪 Testing Dashboard API")
    print("=" * 50)
    
    try:
        # Test the overview endpoint
        url = "http://localhost:5000/api/v1/class/overview"
        print(f"📡 Making request to: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response successful!")
            print(f"📊 Response keys: {list(data.keys())}")
            
            # Check statistics
            if 'statistics' in data:
                stats = data['statistics']
                print(f"👥 Total Students: {stats.get('total_students', 'N/A')}")
                print(f"📚 Total Subjects: {stats.get('total_subjects', 'N/A')}")
                print(f"📊 Class Average: {stats.get('overall_class_average', 'N/A')}%")
                print(f"📝 Total Assessments: {stats.get('total_assessments', 'N/A')}")
            
            # Check year distribution
            if 'year_distribution' in data:
                print(f"📈 Year Distribution: {data['year_distribution']}")
            
            # Check if we have performance data
            if 'performance_trends' in data:
                print(f"📊 Performance Trends: {len(data['performance_trends'])} data points")
            
            if 'subjects_performance' in data:
                print(f"📚 Subject Performance: {len(data['subjects_performance'])} subjects")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"📋 Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Backend server is not running")
        print("💡 Start the backend with: python run.py")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_dashboard_api()