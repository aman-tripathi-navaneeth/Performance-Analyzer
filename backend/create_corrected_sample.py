#!/usr/bin/env python3
"""
Create corrected sample files with proper column names
"""

import pandas as pd
import os

# Create sample_data directory if it doesn't exist
os.makedirs('sample_data', exist_ok=True)

# Sample data with correct column names
sample_data = [
    # Mathematics - 2nd Year CSE A
    {'Student ID': '22A91A0501', 'Student Name': 'Aarav Sharma', 'Score': 85, 'Email': 'aarav.sharma@college.edu', 'Phone': '9876543210', 'Remarks': 'Good performance'},
    {'Student ID': '22A91A0502', 'Student Name': 'Aditi Patel', 'Score': 92, 'Email': 'aditi.patel@college.edu', 'Phone': '9876543211', 'Remarks': 'Excellent work'},
    {'Student ID': '22A91A0503', 'Student Name': 'Arjun Kumar', 'Score': 78, 'Email': 'arjun.kumar@college.edu', 'Phone': '9876543212', 'Remarks': 'Needs improvement'},
    {'Student ID': '22A91A0504', 'Student Name': 'Ananya Singh', 'Score': 88, 'Email': 'ananya.singh@college.edu', 'Phone': '9876543213', 'Remarks': 'Very good'},
    {'Student ID': '22A91A0505', 'Student Name': 'Akash Gupta', 'Score': 76, 'Email': 'akash.gupta@college.edu', 'Phone': '9876543214', 'Remarks': 'Average performance'},
    {'Student ID': '22A91A0506', 'Student Name': 'Bhavya Reddy', 'Score': 94, 'Email': 'bhavya.reddy@college.edu', 'Phone': '9876543215', 'Remarks': 'Outstanding'},
    {'Student ID': '22A91A0507', 'Student Name': 'Chetan Rao', 'Score': 82, 'Email': 'chetan.rao@college.edu', 'Phone': '9876543216', 'Remarks': 'Good effort'},
    {'Student ID': '22A91A0508', 'Student Name': 'Deepika Jain', 'Score': 90, 'Email': 'deepika.jain@college.edu', 'Phone': '9876543217', 'Remarks': 'Excellent'},
    {'Student ID': '22A91A0509', 'Student Name': 'Dhruv Agarwal', 'Score': 74, 'Email': 'dhruv.agarwal@college.edu', 'Phone': '9876543218', 'Remarks': 'Can do better'},
    {'Student ID': '22A91A0510', 'Student Name': 'Esha Verma', 'Score': 87, 'Email': 'esha.verma@college.edu', 'Phone': '9876543219', 'Remarks': 'Good work'},
    {'Student ID': '22A91A0511', 'Student Name': 'Farhan Ali', 'Score': 79, 'Email': 'farhan.ali@college.edu', 'Phone': '9876543220', 'Remarks': 'Satisfactory'},
    {'Student ID': '22A91A0512', 'Student Name': 'Garima Mehta', 'Score': 91, 'Email': 'garima.mehta@college.edu', 'Phone': '9876543221', 'Remarks': 'Very good'},
    {'Student ID': '22A91A0513', 'Student Name': 'Harsh Bansal', 'Score': 83, 'Email': 'harsh.bansal@college.edu', 'Phone': '9876543222', 'Remarks': 'Good performance'},
    {'Student ID': '22A91A0514', 'Student Name': 'Ishita Kapoor', 'Score': 89, 'Email': 'ishita.kapoor@college.edu', 'Phone': '9876543223', 'Remarks': 'Excellent'},
    {'Student ID': '22A91A0515', 'Student Name': 'Jatin Malhotra', 'Score': 77, 'Email': 'jatin.malhotra@college.edu', 'Phone': '9876543224', 'Remarks': 'Needs focus'},
    {'Student ID': '22A91A0516', 'Student Name': 'Kavya Nair', 'Score': 93, 'Email': 'kavya.nair@college.edu', 'Phone': '9876543225', 'Remarks': 'Outstanding'},
    {'Student ID': '22A91A0517', 'Student Name': 'Laksh Tiwari', 'Score': 81, 'Email': 'laksh.tiwari@college.edu', 'Phone': '9876543226', 'Remarks': 'Good effort'},
    {'Student ID': '22A91A0518', 'Student Name': 'Meera Saxena', 'Score': 86, 'Email': 'meera.saxena@college.edu', 'Phone': '9876543227', 'Remarks': 'Very good'},
    {'Student ID': '22A91A0519', 'Student Name': 'Nikhil Joshi', 'Score': 75, 'Email': 'nikhil.joshi@college.edu', 'Phone': '9876543228', 'Remarks': 'Average'},
    {'Student ID': '22A91A0520', 'Student Name': 'Priya Sinha', 'Score': 88, 'Email': 'priya.sinha@college.edu', 'Phone': '9876543229', 'Remarks': 'Good work'}
]

# Create DataFrame
df = pd.DataFrame(sample_data)

# Save to Excel
filepath = os.path.join('sample_data', 'Test_Mathematics_2nd_Year_CSEA.xlsx')
df.to_excel(filepath, index=False)

print(f"✓ Created {filepath} with {len(sample_data)} students")
print("\nColumn names:")
for col in df.columns:
    print(f"  - {col}")

print("\n📋 How to test:")
print("1. Upload this file with:")
print("   Year: 2nd Year")
print("   Section: CSE A") 
print("   Subject: Mathematics")
print("2. Check if 20 new students appear in dashboard")
print("3. Run debug_database.py to verify data was saved")