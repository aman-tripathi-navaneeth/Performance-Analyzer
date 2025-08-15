#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
# import requests  # Not needed for test client
import json

def test_overview_api():
    """Test the overview API via HTTP request"""
    print("=== TESTING OVERVIEW API VIA HTTP ===")
    
    try:
        # Start the app in test mode
        app = create_app()
        
        with app.test_client() as client:
            # Make a request to the overview endpoint
            response = client.get('/api/v1/class/overview')
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"Response keys: {list(data.keys())}")
                
                if 'data' in data:
                    overview_data = data['data']
                    print(f"Overview data keys: {list(overview_data.keys())}")
                    
                    if 'year_section_distribution' in overview_data:
                        print("✅ year_section_distribution found!")
                        print(f"Distribution: {json.dumps(overview_data['year_section_distribution'], indent=2)}")
                    else:
                        print("❌ year_section_distribution NOT found")
                        
                    if 'year_distribution' in overview_data:
                        print("✅ year_distribution found!")
                        print(f"Year distribution: {json.dumps(overview_data['year_distribution'], indent=2)}")
                    else:
                        print("❌ year_distribution NOT found")
                        
                    # Print all available data for debugging
                    print("\n=== FULL RESPONSE DATA ===")
                    print(json.dumps(data, indent=2, default=str))
                else:
                    print("❌ No 'data' key in response")
            else:
                print(f"❌ Request failed with status {response.status_code}")
                print(f"Response: {response.get_data(as_text=True)}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_overview_api()