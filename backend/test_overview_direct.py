#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.api.analytics import get_class_overview

def test_overview_direct():
    """Test the overview API directly"""
    print("=== TESTING OVERVIEW API DIRECTLY ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Call the function directly
            response_tuple = get_class_overview()
            
            print(f"Response tuple type: {type(response_tuple)}")
            
            if isinstance(response_tuple, tuple):
                response, status_code = response_tuple
                print(f"Status code: {status_code}")
                
                if hasattr(response, 'get_json'):
                    data = response.get_json()
                    print(f"JSON data keys: {list(data.keys()) if data else 'None'}")
                    
                    if data and 'data' in data:
                        overview_data = data['data']
                        print(f"Overview data keys: {list(overview_data.keys())}")
                        
                        if 'year_section_distribution' in overview_data:
                            print("✅ year_section_distribution found!")
                            print(f"Distribution: {overview_data['year_section_distribution']}")
                        else:
                            print("❌ year_section_distribution NOT found")
                            print(f"Available keys: {list(overview_data.keys())}")
                    else:
                        print("❌ No 'data' key in response")
                else:
                    print("❌ Response doesn't have get_json method")
            else:
                print(f"❌ Unexpected response type: {type(response_tuple)}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_overview_direct()