#!/usr/bin/env python3
"""
Test the raw API response to see exactly what's being returned
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
import json

def test_raw_api():
    """Test the raw API response"""
    app = create_app()
    
    with app.app_context():
        print("=== TESTING RAW API RESPONSE ===")
        
        with app.test_client() as client:
            response = client.get('/api/v1/class/overview')
            
            print(f"Status Code: {response.status_code}")
            print(f"Content Type: {response.content_type}")
            
            # Get raw response text
            raw_text = response.get_data(as_text=True)
            print(f"\nRaw Response Length: {len(raw_text)} characters")
            
            try:
                # Parse JSON
                data = json.loads(raw_text)
                print(f"\n✅ JSON Parse Successful")
                print(f"Success: {data.get('success', 'Not found')}")
                
                if 'data' in data:
                    overview_data = data['data']
                    print(f"\nKeys in 'data' object:")
                    for key in sorted(overview_data.keys()):
                        value = overview_data[key]
                        if isinstance(value, dict):
                            print(f"  {key}: dict with {len(value)} keys")
                            if key == 'year_section_distribution':
                                print(f"    Content: {value}")
                        elif isinstance(value, list):
                            print(f"  {key}: list with {len(value)} items")
                        else:
                            print(f"  {key}: {type(value).__name__}")
                    
                    # Specifically check for year_section_distribution
                    if 'year_section_distribution' in overview_data:
                        ysd = overview_data['year_section_distribution']
                        print(f"\n✅ year_section_distribution FOUND!")
                        print(f"Type: {type(ysd)}")
                        print(f"Content: {ysd}")
                        print(f"Is Empty: {not bool(ysd)}")
                    else:
                        print(f"\n❌ year_section_distribution NOT FOUND!")
                        print(f"Available keys: {list(overview_data.keys())}")
                else:
                    print(f"\n❌ No 'data' key in response")
                    print(f"Response keys: {list(data.keys())}")
                    
            except json.JSONDecodeError as e:
                print(f"\n❌ JSON Parse Error: {e}")
                print(f"First 500 chars of response:")
                print(raw_text[:500])

if __name__ == "__main__":
    test_raw_api()