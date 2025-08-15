#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
import json

def debug_overview_response():
    """Debug the overview API response to see exact data structure"""
    print("=== DEBUGGING OVERVIEW API RESPONSE ===")
    
    app = create_app()
    
    with app.test_client() as client:
        response = client.get('/api/v1/class/overview')
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            
            if data.get('success'):
                overview_data = data['data']
                
                print("\n📊 YEAR DISTRIBUTION:")
                year_dist = overview_data.get('year_distribution', {})
                for year, count in year_dist.items():
                    print(f"  {year}: {count} students")
                
                print("\n📚 YEAR/SECTION DISTRIBUTION:")
                year_section_dist = overview_data.get('year_section_distribution', {})
                for year, sections in year_section_dist.items():
                    print(f"  {year}:")
                    for section, count in sections.items():
                        print(f"    - {section}: {count} students")
                
                print("\n🔍 SUBJECTS PERFORMANCE (first 5):")
                subjects = overview_data.get('subjects_performance', [])[:5]
                for subject in subjects:
                    print(f"  - {subject['subject_name']}: {subject['average_percentage']}%")
                
                print(f"\n📈 TOTAL STUDENTS: {overview_data.get('statistics', {}).get('total_students', 0)}")
                
                # Check if any years have 0 students
                print("\n⚠️  ZERO STUDENT YEARS:")
                for year, count in year_dist.items():
                    if count == 0:
                        print(f"  - {year}: {count} students (will be disabled)")
                    else:
                        print(f"  - {year}: {count} students (clickable)")
                        
            else:
                print(f"❌ API Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.get_data(as_text=True)}")

if __name__ == "__main__":
    debug_overview_response()