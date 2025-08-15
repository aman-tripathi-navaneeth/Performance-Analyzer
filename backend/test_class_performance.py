#!/usr/bin/env python3
"""
Test the class performance API endpoint
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
import json

def test_class_performance_api():
    """Test the class performance API endpoint"""
    app = create_app()
    
    with app.app_context():
        print("=== TESTING CLASS PERFORMANCE API ===")
        
        with app.test_client() as client:
            # Test 1: Get class overview to see available classes
            print("\n1. Testing class overview for year/section data...")
            response = client.get('/api/v1/class/overview')
            
            if response.status_code == 200:
                data = response.get_json()
                if data['success']:
                    overview_data = data['data']
                    print(f"   ✅ Overview API successful")
                    
                    # Check if year_section_distribution exists
                    if 'year_section_distribution' in overview_data:
                        year_section_dist = overview_data['year_section_distribution']
                        print(f"   📊 Year/Section Distribution:")
                        for year, sections in year_section_dist.items():
                            print(f"      {year}:")
                            for section, count in sections.items():
                                print(f"        - {section}: {count} students")
                        
                        # Test with first available class
                        if year_section_dist:
                            first_year = list(year_section_dist.keys())[0]
                            first_section = list(year_section_dist[first_year].keys())[0]
                            
                            # Extract year number
                            year_num = first_year.split()[0][0]  # Get first digit
                            
                            print(f"\n2. Testing class performance for {first_year} {first_section}...")
                            perf_response = client.get(f'/api/v1/class/performance/{year_num}/{first_section}')
                            
                            if perf_response.status_code == 200:
                                perf_data = perf_response.get_json()
                                if perf_data['success']:
                                    class_data = perf_data['data']
                                    print(f"   ✅ Class performance API successful")
                                    print(f"   📚 Class: {class_data['class_name']}")
                                    print(f"   📊 Overall Average: {class_data['overall_stats']['overall_average']}%")
                                    print(f"   👥 Total Students: {class_data['overall_stats']['total_students']}")
                                    print(f"   📖 Total Subjects: {class_data['overall_stats']['total_subjects']}")
                                    
                                    print(f"\n   📚 Subject Performance:")
                                    for subject in class_data['subjects_performance'][:3]:  # Show first 3
                                        print(f"      - {subject['base_subject_name']}: {subject['class_average']}% ({subject['grade']})")
                                    
                                    print(f"\n   👥 Top Students:")
                                    for student in class_data['students_list'][:3]:  # Show top 3
                                        print(f"      - {student['full_name']}: {student['average_percentage']}% ({student['grade']})")
                                else:
                                    print(f"   ❌ Class performance API failed: {perf_data['error']}")
                            else:
                                print(f"   ❌ Class performance API error: {perf_response.status_code}")
                        else:
                            print("   ⚠️  No year/section data available for testing")
                    else:
                        print("   ❌ year_section_distribution not found in overview data")
                else:
                    print(f"   ❌ Overview API failed: {data['error']}")
            else:
                print(f"   ❌ Overview API error: {response.status_code}")
        
        print("\n=== CLASS PERFORMANCE API TEST COMPLETED ===")

if __name__ == "__main__":
    test_class_performance_api()