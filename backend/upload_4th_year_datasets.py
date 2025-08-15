#!/usr/bin/env python3
"""
Upload all 4th Year CSE A datasets to test the complete system
"""

import requests
import os
import sys

# API endpoint
UPLOAD_URL = "http://localhost:5000/api/v1/uploads/upload"

# Dataset files for 4th Year CSE A
datasets = [
    "cs401_machine_learning_4th_year_cse_a.csv",
    "cs402_software_engineering_4th_year_cse_a.csv", 
    "cs403_computer_networks_4th_year_cse_a.csv",
    "cs404_database_management_systems_4th_year_cse_a.csv",
    "cs405_artificial_intelligence_4th_year_cse_a.csv",
    "cs406_compiler_design_4th_year_cse_a.csv"
]

def upload_dataset(file_path):
    """Upload a single dataset file"""
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(UPLOAD_URL, files=files)
            
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {os.path.basename(file_path)}: {result.get('message', 'Success')}")
            return True
        else:
            print(f"❌ {os.path.basename(file_path)}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ {os.path.basename(file_path)}: {str(e)}")
        return False

def main():
    print("🚀 Uploading 4th Year CSE A Datasets...")
    print("=" * 50)
    
    sample_data_dir = "sample_data"
    success_count = 0
    
    for dataset in datasets:
        file_path = os.path.join(sample_data_dir, dataset)
        if os.path.exists(file_path):
            if upload_dataset(file_path):
                success_count += 1
        else:
            print(f"❌ File not found: {file_path}")
    
    print("=" * 50)
    print(f"📊 Upload Summary: {success_count}/{len(datasets)} datasets uploaded successfully")
    
    if success_count == len(datasets):
        print("🎉 All datasets uploaded! Ready to test the system.")
    else:
        print("⚠️  Some uploads failed. Check the errors above.")

if __name__ == "__main__":
    main()