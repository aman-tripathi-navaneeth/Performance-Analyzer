#!/usr/bin/env python3
"""
Create a comprehensive test file with 60 students
"""

import pandas as pd
import random
import os

# Create sample_data directory if it doesn't exist
os.makedirs('sample_data', exist_ok=True)

# Comprehensive list of 60 students
students_data = [
    # 2nd Year CSE A (20 students)
    {'Student Name': 'Aarav Sharma', 'Student ID': '22A91A0501', 'Score': 85, 'Email': 'aarav.sharma@college.edu', 'Phone': '9876543210', 'Remarks': 'Good performance'},
    {'Student Name': 'Aditi Patel', 'Student ID': '22A91A0502', 'Score': 92, 'Email': 'aditi.patel@college.edu', 'Phone': '9876543211', 'Remarks': 'Excellent work'},
    {'Student Name': 'Arjun Kumar', 'Student ID': '22A91A0503', 'Score': 78, 'Email': 'arjun.kumar@college.edu', 'Phone': '9876543212', 'Remarks': 'Needs improvement'},
    {'Student Name': 'Ananya Singh', 'Student ID': '22A91A0504', 'Score': 88, 'Email': 'ananya.singh@college.edu', 'Phone': '9876543213', 'Remarks': 'Very good'},
    {'Student Name': 'Akash Gupta', 'Student ID': '22A91A0505', 'Score': 76, 'Email': 'akash.gupta@college.edu', 'Phone': '9876543214', 'Remarks': 'Average performance'},
    {'Student Name': 'Bhavya Reddy', 'Student ID': '22A91A0506', 'Score': 94, 'Email': 'bhavya.reddy@college.edu', 'Phone': '9876543215', 'Remarks': 'Outstanding'},
    {'Student Name': 'Chetan Rao', 'Student ID': '22A91A0507', 'Score': 82, 'Email': 'chetan.rao@college.edu', 'Phone': '9876543216', 'Remarks': 'Good effort'},
    {'Student Name': 'Deepika Jain', 'Student ID': '22A91A0508', 'Score': 90, 'Email': 'deepika.jain@college.edu', 'Phone': '9876543217', 'Remarks': 'Excellent'},
    {'Student Name': 'Dhruv Agarwal', 'Student ID': '22A91A0509', 'Score': 74, 'Email': 'dhruv.agarwal@college.edu', 'Phone': '9876543218', 'Remarks': 'Can do better'},
    {'Student Name': 'Esha Verma', 'Student ID': '22A91A0510', 'Score': 87, 'Email': 'esha.verma@college.edu', 'Phone': '9876543219', 'Remarks': 'Good work'},
    {'Student Name': 'Farhan Ali', 'Student ID': '22A91A0511', 'Score': 79, 'Email': 'farhan.ali@college.edu', 'Phone': '9876543220', 'Remarks': 'Satisfactory'},
    {'Student Name': 'Garima Mehta', 'Student ID': '22A91A0512', 'Score': 91, 'Email': 'garima.mehta@college.edu', 'Phone': '9876543221', 'Remarks': 'Very good'},
    {'Student Name': 'Harsh Bansal', 'Student ID': '22A91A0513', 'Score': 83, 'Email': 'harsh.bansal@college.edu', 'Phone': '9876543222', 'Remarks': 'Good performance'},
    {'Student Name': 'Ishita Kapoor', 'Student ID': '22A91A0514', 'Score': 89, 'Email': 'ishita.kapoor@college.edu', 'Phone': '9876543223', 'Remarks': 'Excellent'},
    {'Student Name': 'Jatin Malhotra', 'Student ID': '22A91A0515', 'Score': 77, 'Email': 'jatin.malhotra@college.edu', 'Phone': '9876543224', 'Remarks': 'Needs focus'},
    {'Student Name': 'Kavya Nair', 'Student ID': '22A91A0516', 'Score': 93, 'Email': 'kavya.nair@college.edu', 'Phone': '9876543225', 'Remarks': 'Outstanding'},
    {'Student Name': 'Laksh Tiwari', 'Student ID': '22A91A0517', 'Score': 81, 'Email': 'laksh.tiwari@college.edu', 'Phone': '9876543226', 'Remarks': 'Good effort'},
    {'Student Name': 'Meera Saxena', 'Student ID': '22A91A0518', 'Score': 86, 'Email': 'meera.saxena@college.edu', 'Phone': '9876543227', 'Remarks': 'Very good'},
    {'Student Name': 'Nikhil Joshi', 'Student ID': '22A91A0519', 'Score': 75, 'Email': 'nikhil.joshi@college.edu', 'Phone': '9876543228', 'Remarks': 'Average'},
    {'Student Name': 'Priya Sinha', 'Student ID': '22A91A0520', 'Score': 88, 'Email': 'priya.sinha@college.edu', 'Phone': '9876543229', 'Remarks': 'Good work'},
    
    # 2nd Year CSE B (20 students)
    {'Student Name': 'Rahul Sharma', 'Student ID': '22A91B0501', 'Score': 82, 'Email': 'rahul.sharma@college.edu', 'Phone': '9876543230', 'Remarks': 'Good coding skills'},
    {'Student Name': 'Sneha Patel', 'Student ID': '22A91B0502', 'Score': 95, 'Email': 'sneha.patel@college.edu', 'Phone': '9876543231', 'Remarks': 'Excellent algorithms'},
    {'Student Name': 'Vikram Kumar', 'Student ID': '22A91B0503', 'Score': 79, 'Email': 'vikram.kumar@college.edu', 'Phone': '9876543232', 'Remarks': 'Needs practice'},
    {'Student Name': 'Pooja Singh', 'Student ID': '22A91B0504', 'Score': 91, 'Email': 'pooja.singh@college.edu', 'Phone': '9876543233', 'Remarks': 'Very good logic'},
    {'Student Name': 'Rohit Gupta', 'Student ID': '22A91B0505', 'Score': 77, 'Email': 'rohit.gupta@college.edu', 'Phone': '9876543234', 'Remarks': 'Average performance'},
    {'Student Name': 'Shruti Reddy', 'Student ID': '22A91B0506', 'Score': 93, 'Email': 'shruti.reddy@college.edu', 'Phone': '9876543235', 'Remarks': 'Outstanding work'},
    {'Student Name': 'Karan Rao', 'Student ID': '22A91B0507', 'Score': 84, 'Email': 'karan.rao@college.edu', 'Phone': '9876543236', 'Remarks': 'Good understanding'},
    {'Student Name': 'Nisha Jain', 'Student ID': '22A91B0508', 'Score': 89, 'Email': 'nisha.jain@college.edu', 'Phone': '9876543237', 'Remarks': 'Excellent'},
    {'Student Name': 'Siddharth Agarwal', 'Student ID': '22A91B0509', 'Score': 75, 'Email': 'siddharth.agarwal@college.edu', 'Phone': '9876543238', 'Remarks': 'Can improve'},
    {'Student Name': 'Riya Verma', 'Student ID': '22A91B0510', 'Score': 88, 'Email': 'riya.verma@college.edu', 'Phone': '9876543239', 'Remarks': 'Good work'},
    {'Student Name': 'Aryan Ali', 'Student ID': '22A91B0511', 'Score': 80, 'Email': 'aryan.ali@college.edu', 'Phone': '9876543240', 'Remarks': 'Satisfactory'},
    {'Student Name': 'Tanya Mehta', 'Student ID': '22A91B0512', 'Score': 92, 'Email': 'tanya.mehta@college.edu', 'Phone': '9876543241', 'Remarks': 'Very good'},
    {'Student Name': 'Varun Bansal', 'Student ID': '22A91B0513', 'Score': 85, 'Email': 'varun.bansal@college.edu', 'Phone': '9876543242', 'Remarks': 'Good performance'},
    {'Student Name': 'Kritika Kapoor', 'Student ID': '22A91B0514', 'Score': 90, 'Email': 'kritika.kapoor@college.edu', 'Phone': '9876543243', 'Remarks': 'Excellent'},
    {'Student Name': 'Yash Malhotra', 'Student ID': '22A91B0515', 'Score': 78, 'Email': 'yash.malhotra@college.edu', 'Phone': '9876543244', 'Remarks': 'Needs focus'},
    {'Student Name': 'Divya Nair', 'Student ID': '22A91B0516', 'Score': 94, 'Email': 'divya.nair@college.edu', 'Phone': '9876543245', 'Remarks': 'Outstanding'},
    {'Student Name': 'Aditya Tiwari', 'Student ID': '22A91B0517', 'Score': 83, 'Email': 'aditya.tiwari@college.edu', 'Phone': '9876543246', 'Remarks': 'Good effort'},
    {'Student Name': 'Sakshi Saxena', 'Student ID': '22A91B0518', 'Score': 87, 'Email': 'sakshi.saxena@college.edu', 'Phone': '9876543247', 'Remarks': 'Very good'},
    {'Student Name': 'Manish Joshi', 'Student ID': '22A91B0519', 'Score': 76, 'Email': 'manish.joshi@college.edu', 'Phone': '9876543248', 'Remarks': 'Average'},
    {'Student Name': 'Neha Sinha', 'Student ID': '22A91B0520', 'Score': 89, 'Email': 'neha.sinha@college.edu', 'Phone': '9876543249', 'Remarks': 'Good work'},
    
    # 1st Year CSM (20 students)
    {'Student Name': 'Abhishek Kumar', 'Student ID': '21A91M0501', 'Score': 73, 'Email': 'abhishek.kumar@college.edu', 'Phone': '9876543250', 'Remarks': 'Good basics'},
    {'Student Name': 'Anjali Sharma', 'Student ID': '21A91M0502', 'Score': 86, 'Email': 'anjali.sharma@college.edu', 'Phone': '9876543251', 'Remarks': 'Excellent understanding'},
    {'Student Name': 'Rajesh Patel', 'Student ID': '21A91M0503', 'Score': 69, 'Email': 'rajesh.patel@college.edu', 'Phone': '9876543252', 'Remarks': 'Needs improvement'},
    {'Student Name': 'Swati Singh', 'Student ID': '21A91M0504', 'Score': 82, 'Email': 'swati.singh@college.edu', 'Phone': '9876543253', 'Remarks': 'Very good'},
    {'Student Name': 'Amit Gupta', 'Student ID': '21A91M0505', 'Score': 67, 'Email': 'amit.gupta@college.edu', 'Phone': '9876543254', 'Remarks': 'Average work'},
    {'Student Name': 'Priyanka Reddy', 'Student ID': '21A91M0506', 'Score': 88, 'Email': 'priyanka.reddy@college.edu', 'Phone': '9876543255', 'Remarks': 'Outstanding'},
    {'Student Name': 'Deepak Rao', 'Student ID': '21A91M0507', 'Score': 75, 'Email': 'deepak.rao@college.edu', 'Phone': '9876543256', 'Remarks': 'Good effort'},
    {'Student Name': 'Kavita Jain', 'Student ID': '21A91M0508', 'Score': 84, 'Email': 'kavita.jain@college.edu', 'Phone': '9876543257', 'Remarks': 'Excellent'},
    {'Student Name': 'Suresh Agarwal', 'Student ID': '21A91M0509', 'Score': 71, 'Email': 'suresh.agarwal@college.edu', 'Phone': '9876543258', 'Remarks': 'Can do better'},
    {'Student Name': 'Rekha Verma', 'Student ID': '21A91M0510', 'Score': 79, 'Email': 'rekha.verma@college.edu', 'Phone': '9876543259', 'Remarks': 'Good work'},
    {'Student Name': 'Mohit Ali', 'Student ID': '21A91M0511', 'Score': 72, 'Email': 'mohit.ali@college.edu', 'Phone': '9876543260', 'Remarks': 'Satisfactory'},
    {'Student Name': 'Sunita Mehta', 'Student ID': '21A91M0512', 'Score': 85, 'Email': 'sunita.mehta@college.edu', 'Phone': '9876543261', 'Remarks': 'Very good'},
    {'Student Name': 'Ravi Bansal', 'Student ID': '21A91M0513', 'Score': 78, 'Email': 'ravi.bansal@college.edu', 'Phone': '9876543262', 'Remarks': 'Good performance'},
    {'Student Name': 'Geeta Kapoor', 'Student ID': '21A91M0514', 'Score': 83, 'Email': 'geeta.kapoor@college.edu', 'Phone': '9876543263', 'Remarks': 'Excellent'},
    {'Student Name': 'Naveen Malhotra', 'Student ID': '21A91M0515', 'Score': 70, 'Email': 'naveen.malhotra@college.edu', 'Phone': '9876543264', 'Remarks': 'Needs focus'},
    {'Student Name': 'Seema Nair', 'Student ID': '21A91M0516', 'Score': 87, 'Email': 'seema.nair@college.edu', 'Phone': '9876543265', 'Remarks': 'Outstanding'},
    {'Student Name': 'Ajay Tiwari', 'Student ID': '21A91M0517', 'Score': 76, 'Email': 'ajay.tiwari@college.edu', 'Phone': '9876543266', 'Remarks': 'Good effort'},
    {'Student Name': 'Madhuri Saxena', 'Student ID': '21A91M0518', 'Score': 81, 'Email': 'madhuri.saxena@college.edu', 'Phone': '9876543267', 'Remarks': 'Very good'},
    {'Student Name': 'Vinod Joshi', 'Student ID': '21A91M0519', 'Score': 68, 'Email': 'vinod.joshi@college.edu', 'Phone': '9876543268', 'Remarks': 'Average'},
    {'Student Name': 'Lata Sinha', 'Student ID': '21A91M0520', 'Score': 80, 'Email': 'lata.sinha@college.edu', 'Phone': '9876543269', 'Remarks': 'Good work'}
]

# Create DataFrame
df = pd.DataFrame(students_data)

# Save to Excel
filepath = os.path.join('sample_data', 'Comprehensive_Test_60_Students.xlsx')
df.to_excel(filepath, index=False)

print(f"✓ Created {filepath} with {len(students_data)} students")
print("\n📊 Student Distribution:")
print("- 2nd Year CSE A: 20 students (22A91A0501-0520)")
print("- 2nd Year CSE B: 20 students (22A91B0501-0520)")
print("- 1st Year CSM: 20 students (21A91M0501-0520)")
print(f"\nTotal: {len(students_data)} students")

print("\n📋 How to use this file:")
print("1. Upload as '2nd Year' + 'CSE A' + 'Mathematics' (first 20 students)")
print("2. Upload as '2nd Year' + 'CSE B' + 'Programming' (next 20 students)")
print("3. Upload as '1st Year' + 'CSM' + 'Chemistry' (last 20 students)")
print("Or create separate files for each section if needed.")