#!/usr/bin/env python3
"""
Convert CSV sample files to Excel format for upload testing
"""

import pandas as pd
import os

def convert_csv_to_excel():
    """Convert CSV files to Excel format"""
    
    # List of CSV files to convert
    csv_files = [
        'sample_upload_data.csv',
        'sample_multiple_assessments.csv'
    ]
    
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            # Read CSV file
            df = pd.read_csv(csv_file)
            
            # Create Excel filename
            excel_file = csv_file.replace('.csv', '.xlsx')
            
            # Save as Excel
            df.to_excel(excel_file, index=False)
            
            print(f"✅ Converted {csv_file} to {excel_file}")
            print(f"   📊 Rows: {len(df)}, Columns: {len(df.columns)}")
            print(f"   📁 File: {excel_file}")
            print()
        else:
            print(f"❌ File not found: {csv_file}")
    
    print("🎯 Upload Instructions:")
    print("1. Use the generated .xlsx files")
    print("2. Login to http://localhost:3000")
    print("3. Go to Upload page")
    print("4. Select subject name (e.g., 'Test Mathematics')")
    print("5. Choose subject type: 'regular'")
    print("6. Upload the Excel file")
    print("7. Check Students page for results!")

if __name__ == '__main__':
    convert_csv_to_excel() 