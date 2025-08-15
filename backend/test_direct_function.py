#!/usr/bin/env python3
"""
Test the analytics function directly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.api.analytics import get_class_overview

def test_direct_function():
    """Test the function directly"""
    app = create_app()
    
    with app.app_context():
        print("=== TESTING DIRECT FUNCTION CALL ===")
        
        # Call the function directly
        response, status_code = get_class_overview()
        
        print(f"Status Code: {status_code}")
        print(f"Response Type: {type(response)}")
        
        # Get the JSON data
        json_data = response.get_json()
        print(f"JSON Success: {json_data.get('success', 'Not found')}")
        
        if 'data' in json_data:
            overview_data = json_data['data']
            print(f"\nKeys in response data:")
            for key in sorted(overview_data.keys()):
                print(f"  {key}")
            
            if 'year_section_distribution' in overview_data:
                print(f"\n✅ year_section_distribution FOUND in direct call!")
                print(f"Content: {overview_data['year_section_distribution']}")
            else:
                print(f"\n❌ year_section_distribution NOT FOUND in direct call!")
        else:
            print(f"\n❌ No 'data' key in response")

if __name__ == "__main__":
    test_direct_function()