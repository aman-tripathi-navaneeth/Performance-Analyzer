"""
Test script for the updated upload functionality
Creates sample data to test year and section based uploads
"""

import requests
import json
import os
from io import BytesIO
import pandas as pd

def create_sample_excel():
    """Create a sample Excel file for testing"""
    data = {
        'Student Name': [
            'John Doe',
            'Jane Smith', 
            'Mike Johnson',
            'Sarah Wilson',
            'David Brown'
        ],
        'Student ID': [
            '21A91A0501',
            '21A91A0502',
            '21A91A0503',
            '21A91A0504',
            '21A91A0505'
        ],
        'Score': [85, 92, 78, 88, 95],
        'Email': [
            'john.doe@college.edu',
            'jane.smith@college.edu',
            'mike.johnson@college.edu',
            'sarah.wilson@college.edu',
            'david.brown@college.edu'
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Save to Excel file
    filename = 'sample_data_structures_2nd_year_csea.xlsx'
    df.to_excel(filename, index=False)
    return filename

def test_upload():
    """Test the upload API with year and section"""
    
    # Create sample file
    filename = create_sample_excel()
    
    try:
        # Prepare upload data
        url = 'http://localhost:5000/api/v1/upload/subject'
        
        # Test data for 2nd year CSE A Data Structures
        data = {
            'subjectName': 'Data Structures',
            'year': '2',
            'section': 'CSEA',
            'assessmentType': 'Mid-term Exam'
        }
        
        # Upload file
        with open(filename, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, data=data, files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Upload successful!")
        else:
            print("❌ Upload failed!")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)

def test_multiple_uploads():
    """Test multiple uploads for different years and sections"""
    
    test_cases = [
        {
            'subjectName': 'Mathematics',
            'year': '1',
            'section': 'CSEA',
            'assessmentType': 'Quiz'
        },
        {
            'subjectName': 'Physics',
            'year': '1',
            'section': 'ECE',
            'assessmentType': 'Lab Test'
        },
        {
            'subjectName': 'Database Systems',
            'year': '3',
            'section': 'CSEB',
            'assessmentType': 'Final Exam'
        },
        {
            'subjectName': 'Computer Networks',
            'year': '4',
            'section': 'CSM',
            'assessmentType': 'Project'
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n--- Test Case {i+1}: {test_case['subjectName']} Year {test_case['year']} {test_case['section']} ---")
        
        # Create sample file for this test case
        filename = create_sample_excel()
        
        try:
            url = 'http://localhost:5000/api/v1/upload/subject'
            
            with open(filename, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, data=test_case, files=files)
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: {result.get('message', 'Upload completed')}")
                if 'data' in result:
                    print(f"   Records created: {result['data'].get('records_created', 0)}")
                    print(f"   Students processed: {result['data'].get('students_processed', 0)}")
            else:
                print(f"❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        finally:
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == "__main__":
    print("Testing Upload API with Year and Section Structure")
    print("=" * 50)
    
    # Test single upload
    print("\n1. Testing single upload...")
    test_upload()
    
    # Test multiple uploads
    print("\n2. Testing multiple uploads...")
    test_multiple_uploads()
    
    print("\n" + "=" * 50)
    print("Testing completed!")