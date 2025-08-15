#!/usr/bin/env python3
"""
Test script to check what the API is returning
"""

import requests
import json

def test_api():
    try:
        # Test the class overview endpoint
        response = requests.get('http://localhost:5000/api/v1/class/overview')
        
        if response.status_code == 200:
            data = response.json()
            print("=== API RESPONSE ===")
            print(json.dumps(data, indent=2))
            
            if 'data' in data:
                stats = data['data'].get('statistics', {})
                print(f"\n=== SUMMARY ===")
                print(f"Total Students: {stats.get('total_students', 0)}")
                print(f"Total Subjects: {stats.get('total_subjects', 0)}")
                print(f"Total Assessments: {stats.get('total_assessments', 0)}")
                print(f"Overall Average: {stats.get('overall_class_average', 0)}%")
                
                subjects = data['data'].get('subjects_performance', [])
                print(f"\n=== SUBJECTS ({len(subjects)}) ===")
                for subject in subjects:
                    print(f"- {subject.get('subject_name')}: {subject.get('average_percentage')}% avg")
        else:
            print(f"API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_api()