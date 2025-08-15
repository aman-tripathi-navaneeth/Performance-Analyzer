#!/usr/bin/env python3
"""
Test the class overview API to check year_section_distribution
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
import json

def test_overview_api():
    """Test the class overview API"""
    app = create_app()
    
    with app.app_context():
        print("=== TESTING CLASS OVERVIEW API ===")
        
        with app.test_client() as client:
            response = client.get('/api/v1/class/overview')
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ API Response Status: {response.status_code}")
                print(f"✅ Success: {data.get('success', False)}")
                
                if data['success']:
                    overview_data = data['data']
                    print(f"\n📊 Available Keys in Response:")
                    for key in overview_data.keys():
                        print(f"   - {key}")
                    
                    if 'year_section_distribution' in overview_data:
                        print(f"\n✅ year_section_distribution found!")
                        year_section_dist = overview_data['year_section_distribution']
                        print(f"📊 Year/Section Distribution:")
                        for year, sections in year_section_dist.items():
                            print(f"   {year}:")
                            for section, count in sections.items():
                                print(f"     - {section}: {count} students")
                    else:
                        print(f"\n❌ year_section_distribution NOT found!")
                        print(f"Available keys: {list(overview_data.keys())}")
                else:
                    print(f"❌ API Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.get_data(as_text=True)}")

if __name__ == "__main__":
    test_overview_api()