# All Pandas-related logic
import pandas as pd
import numpy as np
import os
from werkzeug.utils import secure_filename
from app.config import Config

def parse_excel_file(file_path):
    """
    Core data processing function that loads Excel data into a DataFrame
    and performs initial data cleaning and validation with robust error handling.
    """
    import logging
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Starting to parse Excel file: {file_path}")
        
        # Load Excel file into DataFrame
        try:
            df = pd.read_excel(file_path)
            logger.info(f"Successfully loaded Excel file with shape: {df.shape}")
        except FileNotFoundError:
            logger.error(f"Excel file not found: {file_path}")
            raise Exception(f"Excel file not found: {file_path}")
        except pd.errors.EmptyDataError:
            logger.error("Excel file is empty")
            raise Exception("Excel file is empty")
        except pd.errors.ParserError as e:
            logger.error(f"Error parsing Excel file - file may be corrupted: {str(e)}")
            raise Exception(f"Error parsing Excel file - file may be corrupted: {str(e)}")
        except PermissionError:
            logger.error(f"Permission denied accessing file: {file_path}")
            raise Exception(f"Permission denied accessing file: {file_path}")
        except Exception as e:
            logger.error(f"Unexpected error loading Excel file: {str(e)}")
            raise Exception(f"Unexpected error loading Excel file: {str(e)}")
        
        # Data cleaning steps with error handling
        try:
            # 1. Standardize column headers - convert to lowercase and strip whitespace
            logger.info("Standardizing column headers")
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # 2. Check for missing values
            missing_values = df.isnull().sum()
            logger.info(f"Missing values per column:\n{missing_values}")
            
            # 3. Ensure data types are correct for numeric columns
            logger.info("Converting numeric columns")
            student_info_cols = ['student_id', 'student_roll_number', 'name', 'first_name', 'last_name']
            
            for col in df.columns:
                if col not in student_info_cols:
                    try:
                        # Try to convert to numeric, errors='coerce' will set invalid values to NaN
                        original_dtype = df[col].dtype
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                        if original_dtype != df[col].dtype:
                            logger.info(f"Converted column '{col}' from {original_dtype} to numeric")
                    except Exception as col_error:
                        logger.warning(f"Could not convert column '{col}' to numeric: {str(col_error)}")
            
            # 4. Remove completely empty rows
            initial_rows = len(df)
            df = df.dropna(how='all')
            removed_rows = initial_rows - len(df)
            if removed_rows > 0:
                logger.info(f"Removed {removed_rows} completely empty rows")
            
            # 5. Remove completely empty columns
            initial_cols = len(df.columns)
            df = df.dropna(axis=1, how='all')
            removed_cols = initial_cols - len(df.columns)
            if removed_cols > 0:
                logger.info(f"Removed {removed_cols} completely empty columns")
            
            # 6. Basic data validation
            if df.empty:
                logger.error("DataFrame is empty after cleaning")
                raise ValueError("Excel file is empty or contains no valid data after cleaning")
            
            # 7. Log final data info
            logger.info(f"DataFrame shape after cleaning: {df.shape}")
            logger.info(f"Column names: {list(df.columns)}")
            logger.info(f"Data types:\n{df.dtypes}")
            
            return df
            
        except ValueError as ve:
            logger.error(f"Data validation error: {str(ve)}")
            raise Exception(f"Data validation error: {str(ve)}")
        except Exception as cleaning_error:
            logger.error(f"Error during data cleaning: {str(cleaning_error)}")
            raise Exception(f"Error during data cleaning: {str(cleaning_error)}")
            
    except Exception as e:
        logger.error(f"Fatal error in parse_excel_file: {str(e)}")
        raise Exception(f"Error parsing Excel file: {str(e)}")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def process_excel_file(file_path, subject_name, subject_type):
    """Process uploaded Excel file and extract student performance data"""
    try:
        # Use the enhanced parse_excel_file function
        df = parse_excel_file(file_path)
        
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
    
    # Expected columns: student_id, name, mid_term, unit_test_1, unit_test_2, etc.
    required_cols = ['student_id', 'name']
    
    # Check if required columns exist (after standardization)
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise Exception(f"Missing required columns: {missing_cols}")
    
    for _, row in df.iterrows():
        student_id = str(row['student_id']).strip()
        student_name = str(row['name']).strip()
        
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
                        'data_type': col.replace('_', ' ').title(),
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
    
    required_cols = ['student_id', 'name', 'week']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise Exception(f"Missing required columns for CRT data: {missing_cols}")
    
    for _, row in df.iterrows():
        student_id = str(row['student_id']).strip()
        student_name = str(row['name']).strip()
        week_number = row['week']
        
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
    
    required_cols = ['student_id', 'name', 'problems_solved']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise Exception(f"Missing required columns for programming data: {missing_cols}")
    
    for _, row in df.iterrows():
        student_id = str(row['student_id']).strip()
        student_name = str(row['name']).strip()
        problems_solved = row['problems_solved']
        
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
def handle_recurring_assessments(subject_name, assessment_name, new_df):
    """
    Handle recurring assessments (like CRT) by merging new data with historical data.
    Queries database for existing records, loads them into DataFrame, and merges with new data.
    """
    import logging
    from app.models import db, Subject, Assessment, PerformanceRecord, Student
    
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Processing recurring assessment: {assessment_name} for subject: {subject_name}")
        
        # Find the subject
        subject = Subject.query.filter_by(subject_name=subject_name).first()
        if not subject:
            logger.warning(f"Subject not found: {subject_name}")
            return new_df, {"historical_records": 0, "merged_records": 0}
        
        # Find existing assessments with the same name
        existing_assessments = Assessment.query.filter_by(
            subject_id=subject.id,
            assessment_name=assessment_name
        ).all()
        
        if not existing_assessments:
            logger.info("No existing assessments found - this is the first upload")
            return new_df, {"historical_records": 0, "merged_records": len(new_df)}
        
        # Query all existing performance records for these assessments
        assessment_ids = [a.id for a in existing_assessments]
        
        historical_records = db.session.query(
            PerformanceRecord.marks_obtained,
            PerformanceRecord.raw_data_from_excel,
            PerformanceRecord.created_at,
            Student.student_roll_number,
            Student.first_name,
            Student.last_name,
            Assessment.assessment_name,
            Assessment.assessment_date,
            Assessment.max_marks
        ).join(
            Student, PerformanceRecord.student_id == Student.id
        ).join(
            Assessment, PerformanceRecord.assessment_id == Assessment.id
        ).filter(
            Assessment.id.in_(assessment_ids)
        ).all()
        
        logger.info(f"Found {len(historical_records)} historical records")
        
        if not historical_records:
            return new_df, {"historical_records": 0, "merged_records": len(new_df)}
        
        # Convert historical records to DataFrame
        historical_data = []
        for record in historical_records:
            row_data = {
                'student_roll_number': record.student_roll_number,
                'first_name': record.first_name,
                'last_name': record.last_name,
                'marks_obtained': record.marks_obtained,
                'assessment_name': record.assessment_name,
                'assessment_date': record.assessment_date,
                'max_marks': record.max_marks,
                'created_at': record.created_at,
                'data_source': 'historical'
            }
            
            # Add raw Excel data if available
            if record.raw_data_from_excel:
                row_data.update(record.raw_data_from_excel)
            
            historical_data.append(row_data)
        
        historical_df = pd.DataFrame(historical_data)
        
        # Prepare new data for merging
        new_df_copy = new_df.copy()
        new_df_copy['data_source'] = 'new'
        new_df_copy['created_at'] = pd.Timestamp.now()
        
        # Standardize column names for merging
        if 'student_id' in new_df_copy.columns:
            new_df_copy['student_roll_number'] = new_df_copy['student_id']
        
        # Handle marks column naming
        marks_columns = ['marks', 'score', 'marks_obtained']
        for col in marks_columns:
            if col in new_df_copy.columns:
                new_df_copy['marks_obtained'] = new_df_copy[col]
                break
        
        # Merge historical and new data using pandas.concat()
        try:
            # Align columns between historical and new data
            common_columns = list(set(historical_df.columns) & set(new_df_copy.columns))
            
            if not common_columns:
                logger.warning("No common columns found between historical and new data")
                return new_df, {"historical_records": len(historical_records), "merged_records": len(new_df)}
            
            # Select only common columns for merging
            historical_subset = historical_df[common_columns]
            new_subset = new_df_copy[common_columns]
            
            # Concatenate the DataFrames
            merged_df = pd.concat([historical_subset, new_subset], ignore_index=True, sort=False)
            
            # Remove duplicates based on student and assessment, keeping the most recent
            if 'student_roll_number' in merged_df.columns and 'created_at' in merged_df.columns:
                merged_df = merged_df.sort_values('created_at', ascending=False)
                merged_df = merged_df.drop_duplicates(
                    subset=['student_roll_number', 'assessment_name'], 
                    keep='first'
                )
            
            logger.info(f"Successfully merged data. Historical: {len(historical_records)}, New: {len(new_df)}, Merged: {len(merged_df)}")
            
            return merged_df, {
                "historical_records": len(historical_records),
                "new_records": len(new_df),
                "merged_records": len(merged_df),
                "common_columns": common_columns
            }
            
        except Exception as merge_error:
            logger.error(f"Error during DataFrame merge: {str(merge_error)}")
            # Return original new data if merge fails
            return new_df, {"historical_records": len(historical_records), "merged_records": len(new_df), "merge_error": str(merge_error)}
    
    except Exception as e:
        logger.error(f"Error in handle_recurring_assessments: {str(e)}")
        return new_df, {"error": str(e), "merged_records": len(new_df)}

def get_historical_performance_data(subject_name, assessment_name=None, student_roll_number=None):
    """
    Retrieve historical performance data for analysis and visualization.
    Can filter by subject, assessment, and/or student.
    """
    import logging
    from app.models import db, Subject, Assessment, PerformanceRecord, Student
    
    logger = logging.getLogger(__name__)
    
    try:
        # Build query
        query = db.session.query(
            PerformanceRecord.marks_obtained,
            PerformanceRecord.raw_data_from_excel,
            PerformanceRecord.created_at,
            Student.student_roll_number,
            Student.first_name,
            Student.last_name,
            Assessment.assessment_name,
            Assessment.assessment_date,
            Assessment.max_marks,
            Subject.subject_name
        ).join(
            Student, PerformanceRecord.student_id == Student.id
        ).join(
            Assessment, PerformanceRecord.assessment_id == Assessment.id
        ).join(
            Subject, Assessment.subject_id == Subject.id
        )
        
        # Apply filters
        if subject_name:
            query = query.filter(Subject.subject_name == subject_name)
        
        if assessment_name:
            query = query.filter(Assessment.assessment_name == assessment_name)
        
        if student_roll_number:
            query = query.filter(Student.student_roll_number == student_roll_number)
        
        # Execute query
        results = query.all()
        
        # Convert to DataFrame
        data = []
        for record in results:
            row_data = {
                'student_roll_number': record.student_roll_number,
                'first_name': record.first_name,
                'last_name': record.last_name,
                'full_name': f"{record.first_name} {record.last_name}",
                'marks_obtained': record.marks_obtained,
                'assessment_name': record.assessment_name,
                'assessment_date': record.assessment_date,
                'max_marks': record.max_marks,
                'percentage': (record.marks_obtained / record.max_marks * 100) if record.max_marks > 0 else 0,
                'subject_name': record.subject_name,
                'created_at': record.created_at
            }
            
            # Add raw Excel data if available
            if record.raw_data_from_excel:
                row_data.update(record.raw_data_from_excel)
            
            data.append(row_data)
        
        df = pd.DataFrame(data)
        logger.info(f"Retrieved {len(df)} historical performance records")
        
        return df
        
    except Exception as e:
        logger.error(f"Error retrieving historical performance data: {str(e)}")
        return pd.DataFrame()  # Return empty DataFrame on error