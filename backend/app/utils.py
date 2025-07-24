import pandas as pd
import os
from werkzeug.utils import secure_filename
from app.config import Config

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def process_excel_file(file_path, subject_name, subject_type):
    """Process uploaded Excel file and extract student performance data"""
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Expected columns based on subject type
        if subject_type == 'crt':
            return process_crt_data(df, subject_name)
        elif subject_type == 'programming':
            return process_programming_data(df, subject_name)
        else:
            return process_regular_subject_data(df, subject_name)
            
    except Exception as e:
        raise Exception(f"Error processing Excel file: {str(e)}")

def process_regular_subject_data(df, subject_name):
    """Process regular subject data (mid-term, unit tests)"""
    processed_data = []
    
    # Expected columns: Student ID, Name, Mid-term, Unit Test 1, Unit Test 2, etc.
    required_cols = ['Student ID', 'Name']
    
    # Check if required columns exist
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise Exception(f"Missing required columns: {missing_cols}")
    
    for _, row in df.iterrows():
        student_id = str(row['Student ID']).strip()
        student_name = str(row['Name']).strip()
        
        if pd.isna(student_id) or pd.isna(student_name):
            continue
            
        # Process each score column
        for col in df.columns:
            if col not in required_cols and not pd.isna(row[col]):
                try:
                    score = float(row[col])
                    processed_data.append({
                        'student_id': student_id,
                        'student_name': student_name,
                        'subject_name': subject_name,
                        'data_type': col,
                        'score': score,
                        'max_score': 100,  # Default max score
                        'week_number': None
                    })
                except (ValueError, TypeError):
                    continue
    
    return processed_data

def process_crt_data(df, subject_name):
    """Process CRT (weekly) data"""
    processed_data = []
    
    required_cols = ['Student ID', 'Name', 'Week']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise Exception(f"Missing required columns for CRT data: {missing_cols}")
    
    for _, row in df.iterrows():
        student_id = str(row['Student ID']).strip()
        student_name = str(row['Name']).strip()
        week_number = row['Week']
        
        if pd.isna(student_id) or pd.isna(student_name) or pd.isna(week_number):
            continue
        
        # Process score columns
        for col in df.columns:
            if col not in required_cols and not pd.isna(row[col]):
                try:
                    score = float(row[col])
                    processed_data.append({
                        'student_id': student_id,
                        'student_name': student_name,
                        'subject_name': subject_name,
                        'data_type': 'CRT Score',
                        'score': score,
                        'max_score': 100,
                        'week_number': int(week_number)
                    })
                except (ValueError, TypeError):
                    continue
    
    return processed_data

def process_programming_data(df, subject_name):
    """Process competitive programming data"""
    processed_data = []
    
    required_cols = ['Student ID', 'Name', 'Problems Solved']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise Exception(f"Missing required columns for programming data: {missing_cols}")
    
    for _, row in df.iterrows():
        student_id = str(row['Student ID']).strip()
        student_name = str(row['Name']).strip()
        problems_solved = row['Problems Solved']
        
        if pd.isna(student_id) or pd.isna(student_name) or pd.isna(problems_solved):
            continue
        
        try:
            processed_data.append({
                'student_id': student_id,
                'student_name': student_name,
                'subject_name': subject_name,
                'data_type': 'Problems Solved',
                'score': float(problems_solved),
                'max_score': 1000,  # Arbitrary max for programming problems
                'week_number': None
            })
        except (ValueError, TypeError):
            continue
    
    return processed_data

def calculate_percentage(score, max_score):
    """Calculate percentage score"""
    if max_score == 0:
        return 0
    return (score / max_score) * 100

def get_grade(percentage):
    """Convert percentage to grade"""
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B+'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'