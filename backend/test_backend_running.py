#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_backend_running():
    """Test if backend is running and returning correct data"""
    print("=== TESTING BACKEND AVAILABILITY ===")
    
    app = create_app()
    
    with app.test_client() as client:
        # Test overview endpoint
        response = client.get('/api/v1/class/overview')
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            
            if data.get('success'):
                overview_data = data['data']
                year_dist = overview_data.get('year_distribution', {})
                year_section_dist = overview_data.get('year_section_distribution', {})
                
                print("✅ Backend is working correctly")
                print(f"📊 Year Distribution: {year_dist}")
                print(f"📚 Year/Section Distribution: {year_section_dist}")
                
                # Check if we have the expected data
                if '1st Year' in year_dist and year_dist['1st Year'] == 3:
                    print("✅ 1st Year data correct (3 students)")
                else:
                    print(f"❌ 1st Year data incorrect: {year_dist.get('1st Year', 'missing')}")
                    
                if '2nd Year' in year_dist and year_dist['2nd Year'] == 40:
                    print("✅ 2nd Year data correct (40 students)")
                else:
                    print(f"❌ 2nd Year data incorrect: {year_dist.get('2nd Year', 'missing')}")
                    
            else:
                print(f"❌ API returned error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.get_data(as_text=True)}")

if __name__ == "__main__":
    test_backend_running()