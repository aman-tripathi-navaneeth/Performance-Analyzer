#!/usr/bin/env python3
"""
Generate sample Excel files for testing the Performance Analyzer
"""

import pandas as pd
import random
import os

# Create sample_data directory if it doesn't exist
os.makedirs('sample_data', exist_ok=True)

# Sample student names (Indian names)
first_names = [
    'Aarav', 'Aditi', 'Arjun', 'Ananya', 'Akash', 'Bhavya', 'Chetan', 'Deepika', 'Dhruv', 'Esha',
    'Farhan', 'Garima', 'Harsh', 'Ishita', 'Jatin', 'Kavya', 'Laksh', 'Meera', 'Nikhil', 'Priya',
    'Rahul', 'Sneha', 'Vikram', 'Pooja', 'Rohit', 'Shruti', 'Karan', 'Nisha', 'Siddharth', 'Riya',
    'Aryan', 'Tanya', 'Varun', 'Kritika', 'Yash', 'Divya', 'Aditya', 'Sakshi', 'Manish', 'Neha',
    'Abhishek', 'Anjali', 'Rajesh', 'Swati', 'Amit', 'Priyanka', 'Deepak', 'Kavita', 'Suresh', 'Rekha',
    'Mohit', 'Sunita', 'Ravi', 'Geeta', 'Naveen', 'Seema', 'Ajay', 'Madhuri', 'Vinod', 'Lata'
]

last_names = [
    'Sharma', 'Patel', 'Kumar', 'Singh', 'Gupta', 'Reddy', 'Rao', 'Jain', 'Agarwal', 'Verma',
    'Ali', 'Mehta', 'Bansal', 'Kapoor', 'Malhotra', 'Nair', 'Tiwari', 'Saxena', 'Joshi', 'Sinha'
]

def generate_student_data(year, section, num_students=20):
    """Generate student data for a specific year and section"""
    students = []
    
    for i in range(num_students):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        # Generate student ID based on year and section
        if section == 'CSEA':
            section_code = 'A'
        elif section == 'CSEB':
            section_code = 'B'
        elif section == 'CSM':
            section_code = 'M'
        elif section == 'ECE':
            section_code = 'E'
        elif section == 'COS':
            section_code = 'C'
        else:
            section_code = 'X'
        
        student_id = f"{year}{year}A91{section_code}05{i+1:02d}"
        
        student = {
            'Student Name': f"{first_name} {last_name}",
            'Student ID': student_id,
            'Email': f"{first_name.lower()}.{last_name.lower()}@college.edu",
            'Phone': f"987654{3210 + i:04d}"
        }
        students.append(student)
    
    return students

def generate_scores(students, subject_difficulty='medium'):
    """Generate scores based on subject difficulty"""
    scored_students = []
    
    for student in students:
        # Generate scores based on difficulty
        if subject_difficulty == 'easy':
            base_score = random.randint(75, 95)
        elif subject_difficulty == 'medium':
            base_score = random.randint(65, 90)
        elif subject_difficulty == 'hard':
            base_score = random.randint(55, 85)
        else:
            base_score = random.randint(60, 90)
        
        # Add some variation
        score = base_score + random.randint(-5, 5)
        score = max(40, min(100, score))  # Ensure score is between 40-100
        
        # Generate remarks based on score
        if score >= 90:
            remarks = random.choice(['Outstanding', 'Excellent work', 'Exceptional performance'])
        elif score >= 80:
            remarks = random.choice(['Very good', 'Good work', 'Well done'])
        elif score >= 70:
            remarks = random.choice(['Good effort', 'Satisfactory', 'Good performance'])
        elif score >= 60:
            remarks = random.choice(['Average', 'Needs improvement', 'Can do better'])
        else:
            remarks = random.choice(['Needs focus', 'Requires attention', 'Must improve'])
        
        student_copy = student.copy()
        student_copy['Score'] = score
        student_copy['Remarks'] = remarks
        scored_students.append(student_copy)
    
    return scored_students

# Generate sample datasets
datasets = [
    # 2nd Year CSE A
    {
        'filename': 'Mathematics_2nd_Year_CSEA.xlsx',
        'year': 22,
        'section': 'CSEA',
        'subject': 'Mathematics',
        'difficulty': 'medium',
        'students': 20
    },
    {
        'filename': 'Physics_2nd_Year_CSEA.xlsx',
        'year': 22,
        'section': 'CSEA',
        'subject': 'Physics',
        'difficulty': 'hard',
        'students': 20
    },
    {
        'filename': 'Data_Structures_2nd_Year_CSEA.xlsx',
        'year': 22,
        'section': 'CSEA',
        'subject': 'Data Structures',
        'difficulty': 'medium',
        'students': 20
    },
    
    # 2nd Year CSE B
    {
        'filename': 'Mathematics_2nd_Year_CSEB.xlsx',
        'year': 22,
        'section': 'CSEB',
        'subject': 'Mathematics',
        'difficulty': 'medium',
        'students': 20
    },
    {
        'filename': 'Programming_2nd_Year_CSEB.xlsx',
        'year': 22,
        'section': 'CSEB',
        'subject': 'Programming',
        'difficulty': 'easy',
        'students': 20
    },
    
    # 1st Year CSM
    {
        'filename': 'Chemistry_1st_Year_CSM.xlsx',
        'year': 21,
        'section': 'CSM',
        'subject': 'Chemistry',
        'difficulty': 'hard',
        'students': 20
    },
    {
        'filename': 'Mathematics_1st_Year_CSM.xlsx',
        'year': 21,
        'section': 'CSM',
        'subject': 'Mathematics',
        'difficulty': 'medium',
        'students': 20
    },
    
    # 3rd Year ECE
    {
        'filename': 'Electronics_3rd_Year_ECE.xlsx',
        'year': 23,
        'section': 'ECE',
        'subject': 'Electronics',
        'difficulty': 'hard',
        'students': 20
    },
    {
        'filename': 'Signals_3rd_Year_ECE.xlsx',
        'year': 23,
        'section': 'ECE',
        'subject': 'Signals and Systems',
        'difficulty': 'hard',
        'students': 20
    },
    
    # 4th Year COS
    {
        'filename': 'Operating_Systems_4th_Year_COS.xlsx',
        'year': 24,
        'section': 'COS',
        'subject': 'Operating Systems',
        'difficulty': 'medium',
        'students': 20
    }
]

print("Generating sample Excel files...")

for dataset in datasets:
    print(f"Creating {dataset['filename']}...")
    
    # Generate student data
    students = generate_student_data(
        dataset['year'], 
        dataset['section'], 
        dataset['students']
    )
    
    # Add scores
    students_with_scores = generate_scores(students, dataset['difficulty'])
    
    # Create DataFrame
    df = pd.DataFrame(students_with_scores)
    
    # Save to Excel
    filepath = os.path.join('sample_data', dataset['filename'])
    df.to_excel(filepath, index=False)
    
    print(f"✓ Created {filepath} with {len(students_with_scores)} students")

print(f"\n🎉 Generated {len(datasets)} sample Excel files!")
print("\nFiles created in 'sample_data' directory:")
for dataset in datasets:
    print(f"  - {dataset['filename']}")

print("\n📋 How to use these files:")
print("1. Start your backend server: python run.py")
print("2. Start your frontend: npm start")
print("3. Login as teacher or admin")
print("4. Go to Upload page")
print("5. Select appropriate Year and Section")
print("6. Enter the Subject name")
print("7. Upload the corresponding Excel file")
print("\nExample:")
print("- For 'Mathematics_2nd_Year_CSEA.xlsx':")
print("  Year: 2nd Year")
print("  Section: CSE A") 
print("  Subject: Mathematics")