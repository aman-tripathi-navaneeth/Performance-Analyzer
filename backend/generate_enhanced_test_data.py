#!/usr/bin/env python3
"""
Generate enhanced test data with 30 student records for the Performance Analyzer
"""

import pandas as pd
import random
import os
from datetime import datetime, timedelta
import uuid

# Create sample_data directory if it doesn't exist
os.makedirs('sample_data', exist_ok=True)

# Extended student names for 30 students
first_names = [
    'Aarav', 'Aditi', 'Arjun', 'Ananya', 'Akash', 'Bhavya', 'Chetan', 'Deepika', 'Dhruv', 'Esha',
    'Farhan', 'Garima', 'Harsh', 'Ishita', 'Jatin', 'Kavya', 'Laksh', 'Meera', 'Nikhil', 'Priya',
    'Rahul', 'Sneha', 'Vikram', 'Pooja', 'Rohit', 'Shruti', 'Karan', 'Nisha', 'Siddharth', 'Riya',
    'Aryan', 'Tanya', 'Varun', 'Kritika', 'Yash', 'Divya', 'Aditya', 'Sakshi', 'Manish', 'Neha',
    'Abhishek', 'Anjali', 'Rajesh', 'Swati', 'Amit', 'Priyanka', 'Deepak', 'Kavita', 'Suresh', 'Rekha'
]

last_names = [
    'Sharma', 'Patel', 'Kumar', 'Singh', 'Gupta', 'Reddy', 'Rao', 'Jain', 'Agarwal', 'Verma',
    'Ali', 'Mehta', 'Bansal', 'Kapoor', 'Malhotra', 'Nair', 'Tiwari', 'Saxena', 'Joshi', 'Sinha',
    'Mishra', 'Chandra', 'Yadav', 'Shah', 'Chopra', 'Bhatt', 'Pandey', 'Thakur', 'Iyer', 'Menon'
]

def generate_student_data(year, section, num_students=30):
    """Generate student data for a specific year and section"""
    students = []
    
    # Ensure we have enough names
    used_names = set()
    
    for i in range(num_students):
        # Ensure unique names
        while True:
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            full_name = f"{first_name} {last_name}"
            if full_name not in used_names:
                used_names.add(full_name)
                break
        
        # Generate student ID based on year and section
        section_codes = {
            'CSE A': 'A', 'CSEA': 'A',
            'CSE B': 'B', 'CSEB': 'B', 
            'CSM': 'M',
            'ECE': 'E',
            'COS': 'C'
        }
        section_code = section_codes.get(section, 'X')
        
        # Generate realistic student ID
        roll_num = f"{i+1:03d}"
        student_id = f"20{year-1}A91{section_code}05{roll_num}"
        
        student = {
            'Student Name': full_name,
            'Student ID': student_id,
            'Roll Number': f"{year}{section_code}{roll_num}",
            'Email': f"{first_name.lower()}.{last_name.lower()}@college.edu",
            'Phone': f"987654{3210 + i:04d}",
            'Year': year,
            'Section': section
        }
        students.append(student)
    
    return students

def generate_performance_scores(students, subject_info):
    """Generate realistic performance scores with assessment details"""
    scored_students = []
    
    for student in students:
        # Create performance profile for student (some are consistently good, others variable)
        performance_type = random.choices(['excellent', 'good', 'average', 'struggling'], weights=[20, 35, 30, 15])[0]
        
        # Base scores based on performance type
        if performance_type == 'excellent':
            base_range = (85, 98)
        elif performance_type == 'good':
            base_range = (75, 90)
        elif performance_type == 'average':
            base_range = (60, 80)
        else:  # struggling
            base_range = (40, 70)
        
        # Adjust for subject difficulty
        difficulty_modifier = {
            'easy': 5,
            'medium': 0,
            'hard': -8,
            'very_hard': -15
        }
        
        modifier = difficulty_modifier.get(subject_info['difficulty'], 0)
        min_score = max(25, base_range[0] + modifier)
        max_score = min(100, base_range[1] + modifier)
        
        # Generate scores for multiple assessments
        assessments = []
        total_score = 0
        total_weight = 0
        
        # Internal Assessment 1 (20%)
        ia1_score = random.randint(min_score, max_score)
        assessments.append({'type': 'Internal Assessment 1', 'score': ia1_score, 'weight': 0.2})
        total_score += ia1_score * 0.2
        total_weight += 0.2
        
        # Internal Assessment 2 (20%)
        ia2_score = random.randint(min_score, max_score)
        assessments.append({'type': 'Internal Assessment 2', 'score': ia2_score, 'weight': 0.2})
        total_score += ia2_score * 0.2
        total_weight += 0.2
        
        # Assignment/Project (15%)
        assignment_score = random.randint(min_score + 5, max_score)  # Usually slightly higher
        assessments.append({'type': 'Assignment', 'score': assignment_score, 'weight': 0.15})
        total_score += assignment_score * 0.15
        total_weight += 0.15
        
        # Practical/Lab (15%)
        practical_score = random.randint(min_score, max_score)
        assessments.append({'type': 'Practical', 'score': practical_score, 'weight': 0.15})
        total_score += practical_score * 0.15
        total_weight += 0.15
        
        # Final Exam (30%)
        final_score = random.randint(min_score - 5, max_score)
        assessments.append({'type': 'Final Exam', 'score': final_score, 'weight': 0.3})
        total_score += final_score * 0.3
        total_weight += 0.3
        
        # Calculate overall score
        overall_score = round(total_score, 1)
        
        # Generate grade based on score
        if overall_score >= 90:
            grade = 'A+'
        elif overall_score >= 85:
            grade = 'A'
        elif overall_score >= 80:
            grade = 'A-'
        elif overall_score >= 75:
            grade = 'B+'
        elif overall_score >= 70:
            grade = 'B'
        elif overall_score >= 65:
            grade = 'B-'
        elif overall_score >= 60:
            grade = 'C+'
        elif overall_score >= 55:
            grade = 'C'
        elif overall_score >= 50:
            grade = 'C-'
        else:
            grade = 'F'
        
        # Generate remarks based on score and performance trend
        remarks_options = {
            'A+': ['Outstanding performance', 'Exceptional work', 'Excellent understanding'],
            'A': ['Very good work', 'Strong performance', 'Well done'],
            'A-': ['Good effort', 'Solid performance', 'Keep it up'],
            'B+': ['Above average', 'Good work', 'Shows potential'],
            'B': ['Satisfactory', 'Meeting expectations', 'Good effort'],
            'B-': ['Average performance', 'Room for improvement', 'Needs focus'],
            'C+': ['Below average', 'Requires attention', 'Can do better'],
            'C': ['Needs improvement', 'Struggling with concepts', 'Extra help needed'],
            'C-': ['Poor performance', 'Significant gaps', 'Immediate attention required'],
            'F': ['Failing', 'Major intervention needed', 'Not meeting standards']
        }
        
        remarks = random.choice(remarks_options.get(grade, ['Needs evaluation']))
        
        # Generate attendance percentage (correlated with performance)
        if performance_type == 'excellent':
            attendance = random.randint(88, 100)
        elif performance_type == 'good':
            attendance = random.randint(78, 95)
        elif performance_type == 'average':
            attendance = random.randint(65, 85)
        else:
            attendance = random.randint(45, 75)
        
        # Create student record
        student_copy = student.copy()
        student_copy.update({
            'Overall Score': overall_score,
            'Grade': grade,
            'Remarks': remarks,
            'Attendance': f"{attendance}%",
            'IA1_Score': ia1_score,
            'IA2_Score': ia2_score,
            'Assignment_Score': assignment_score,
            'Practical_Score': practical_score,
            'Final_Exam_Score': final_score,
            'Subject': subject_info['name'],
            'Assessment_Date': subject_info.get('date', datetime.now().strftime('%Y-%m-%d')),
            'Max_Marks': 100,
            'Performance_Type': performance_type
        })
        
        scored_students.append(student_copy)
    
    return scored_students

# Enhanced dataset definitions with 30 students each
datasets = [
    # 2nd Year CSE A - Multiple subjects
    {
        'filename': 'Mathematics_2nd_Year_CSE_A_Enhanced.xlsx',
        'year': 2,
        'section': 'CSE A',
        'subject_info': {
            'name': 'Mathematics',
            'difficulty': 'medium',
            'date': '2024-01-15'
        },
        'students': 30
    },
    {
        'filename': 'Data_Structures_2nd_Year_CSE_A_Enhanced.xlsx',
        'year': 2,
        'section': 'CSE A',
        'subject_info': {
            'name': 'Data Structures',
            'difficulty': 'hard',
            'date': '2024-01-20'
        },
        'students': 30
    },
    {
        'filename': 'Database_Management_2nd_Year_CSE_A_Enhanced.xlsx',
        'year': 2,
        'section': 'CSE A',
        'subject_info': {
            'name': 'Database Management Systems',
            'difficulty': 'medium',
            'date': '2024-01-25'
        },
        'students': 30
    },
    {
        'filename': 'Object_Oriented_Programming_2nd_Year_CSE_A_Enhanced.xlsx',
        'year': 2,
        'section': 'CSE A',
        'subject_info': {
            'name': 'Object Oriented Programming',
            'difficulty': 'medium',
            'date': '2024-02-01'
        },
        'students': 30
    },
    {
        'filename': 'Computer_Networks_2nd_Year_CSE_A_Enhanced.xlsx',
        'year': 2,
        'section': 'CSE A',
        'subject_info': {
            'name': 'Computer Networks',
            'difficulty': 'hard',
            'date': '2024-02-05'
        },
        'students': 30
    },
    
    # 3rd Year CSE A
    {
        'filename': 'Operating_Systems_3rd_Year_CSE_A_Enhanced.xlsx',
        'year': 3,
        'section': 'CSE A',
        'subject_info': {
            'name': 'Operating Systems',
            'difficulty': 'hard',
            'date': '2024-01-18'
        },
        'students': 30
    },
    {
        'filename': 'Software_Engineering_3rd_Year_CSE_A_Enhanced.xlsx',
        'year': 3,
        'section': 'CSE A',
        'subject_info': {
            'name': 'Software Engineering',
            'difficulty': 'medium',
            'date': '2024-01-22'
        },
        'students': 30
    },
    {
        'filename': 'Machine_Learning_3rd_Year_CSE_A_Enhanced.xlsx',
        'year': 3,
        'section': 'CSE A',
        'subject_info': {
            'name': 'Machine Learning',
            'difficulty': 'very_hard',
            'date': '2024-02-10'
        },
        'students': 30
    },
    
    # 1st Year CSE A  
    {
        'filename': 'Programming_Fundamentals_1st_Year_CSE_A_Enhanced.xlsx',
        'year': 1,
        'section': 'CSE A',
        'subject_info': {
            'name': 'Programming Fundamentals',
            'difficulty': 'easy',
            'date': '2024-01-12'
        },
        'students': 30
    },
    {
        'filename': 'Digital_Logic_1st_Year_CSE_A_Enhanced.xlsx',
        'year': 1,
        'section': 'CSE A',
        'subject_info': {
            'name': 'Digital Logic Design',
            'difficulty': 'medium',
            'date': '2024-01-16'
        },
        'students': 30
    }
]

print("🚀 Generating enhanced test data with 30 student records...")
print("=" * 60)

created_files = []

for dataset in datasets:
    print(f"Creating {dataset['filename']}...")
    
    # Generate student data
    students = generate_student_data(
        dataset['year'], 
        dataset['section'], 
        dataset['students']
    )
    
    # Add performance scores
    students_with_scores = generate_performance_scores(students, dataset['subject_info'])
    
    # Create DataFrame
    df = pd.DataFrame(students_with_scores)
    
    # Reorder columns for better readability
    column_order = [
        'Student Name', 'Student ID', 'Roll Number', 'Email', 'Phone',
        'Year', 'Section', 'Subject',
        'Overall Score', 'Grade', 'Attendance',
        'IA1_Score', 'IA2_Score', 'Assignment_Score', 'Practical_Score', 'Final_Exam_Score',
        'Remarks', 'Assessment_Date', 'Max_Marks'
    ]
    
    # Reorder columns (keep only existing ones)
    available_columns = [col for col in column_order if col in df.columns]
    other_columns = [col for col in df.columns if col not in column_order]
    df = df[available_columns + other_columns]
    
    # Save to Excel
    filepath = os.path.join('sample_data', dataset['filename'])
    df.to_excel(filepath, index=False)
    created_files.append(filepath)
    
    # Print statistics
    avg_score = df['Overall Score'].mean()
    grade_dist = df['Grade'].value_counts().to_dict()
    
    print(f"✓ Created {filepath}")
    print(f"  📊 {len(students_with_scores)} students, Avg Score: {avg_score:.1f}")
    print(f"  📈 Grade Distribution: {dict(sorted(grade_dist.items()))}")
    print()

print(f"🎉 Successfully generated {len(datasets)} enhanced Excel files!")
print("\n📁 Files created in 'sample_data' directory:")
for filepath in created_files:
    print(f"  - {os.path.basename(filepath)}")

print("\n📋 Upload Instructions:")
print("1. Start backend: python start_dev.py")
print("2. Start frontend: npm start")
print("3. Login and go to Upload page")
print("4. Use these mappings:")
print()

for dataset in datasets:
    print(f"📄 {dataset['filename']}:")
    print(f"   Year: {dataset['year']}")
    print(f"   Section: {dataset['section']}")
    print(f"   Subject: {dataset['subject_info']['name']}")
    print()

print("🎯 Features included:")
print("• 30 diverse student records per file")
print("• Realistic performance distribution")
print("• Multiple assessment types (IA1, IA2, Assignment, Practical, Final)")
print("• Grade calculation and distribution")
print("• Attendance correlation with performance")
print("• Comprehensive student information")
print("• Multiple subjects across different years") 