from flask import Blueprint, request, jsonify, current_app
import os
import pandas as pd
from werkzeug.utils import secure_filename
from app.services.data_processor import parse_excel_file, allowed_file
from app import db
from app.models.performance_models import Student, Subject, Assessment, PerformanceRecord
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/subject', methods=['POST'])
def upload_subject_file():
    """
    Upload and process Excel file with student performance data
    POST /api/v1/upload/subject
    Accepts multipart/form-data with file and metadata
    """
    try:
        logger.info("Received file upload request")
        
        # Check if file is present in request
        if 'file' not in request.files:
            logger.error("No file provided in request")
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Get form data
        subject_name = request.form.get('subjectName')
        year = request.form.get('year')
        section = request.form.get('section')
        assessment_type = request.form.get('assessmentType', 'General Assessment')
        
        # Validate required fields
        if not subject_name:
            return jsonify({
                'success': False,
                'error': 'Subject name is required'
            }), 400
            
        if not year:
            return jsonify({
                'success': False,
                'error': 'Year is required'
            }), 400
            
        if not section:
            return jsonify({
                'success': False,
                'error': 'Section is required'
            }), 400
        
        # Check if file was selected
        if file.filename == '':
            logger.error("No file selected")
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            logger.error(f"Invalid file type: {file.filename}")
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Only Excel files (.xlsx, .xls) are allowed'
            }), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Create unique filename to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        
        # Save file to upload directory
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        try:
            file.save(file_path)
            logger.info(f"File saved successfully: {file_path}")
        except Exception as save_error:
            logger.error(f"Error saving file: {str(save_error)}")
            return jsonify({
                'success': False,
                'error': f'Error saving file: {str(save_error)}'
            }), 500
        
        # Process the Excel file
        try:
            logger.info("Starting to process Excel file")
            df = parse_excel_file(file_path)
            
            # Create or get subject with year and section context
            subject = Subject.query.filter_by(
                base_subject_name=subject_name,
                year=int(year),
                section=section
            ).first()
            
            if not subject:
                subject_full_name = f"{subject_name} - Year {year} {section}"
                subject = Subject(
                    subject_name=subject_full_name,
                    base_subject_name=subject_name,
                    year=int(year),
                    section=section
                )
                db.session.add(subject)
                db.session.flush()  # Get the ID without committing
                logger.info(f"Created new subject: {subject_full_name}")
            
            # Create assessment with year-section context
            assessment_name = f"{assessment_type} - {subject_name} (Year {year} {section})"
            assessment_date_obj = datetime.now().date()
            
            assessment = Assessment(
                assessment_name=assessment_name,
                assessment_date=assessment_date_obj,
                max_marks=100,  # Default max marks
                subject_id=subject.id,
                year=int(year),
                section=section,
                assessment_type=assessment_type
            )
            db.session.add(assessment)
            db.session.flush()  # Get the ID without committing
            logger.info(f"Created new assessment: {assessment_name}")
            
            # Enhanced logic to find or create Student and Assessment records
            students_processed = 0
            students_updated = 0
            records_created = 0
            records_updated = 0
            errors = []
            
            # Check if this is a recurring assessment (like CRT)
            is_recurring = 'crt' in assessment_name.lower() or 'weekly' in assessment_name.lower()
            
            # If recurring, check for existing assessment with same name and subject
            if is_recurring:
                existing_assessment = Assessment.query.filter_by(
                    assessment_name=assessment_name,
                    subject_id=subject.id
                ).first()
                
                if existing_assessment:
                    assessment = existing_assessment
                    logger.info(f"Using existing recurring assessment: {assessment_name}")
                else:
                    logger.info(f"Creating new recurring assessment: {assessment_name}")
            
            # Process each row in the DataFrame
            for index, row in df.iterrows():
                try:
                    # Extract student information with multiple fallback options
                    student_roll_number = str(row.get('student_id', row.get('roll_number', row.get('id', '')))).strip()
                    first_name = str(row.get('first_name', '')).strip()
                    last_name = str(row.get('last_name', '')).strip()
                    
                    # Handle case where name is in a single column
                    if not first_name and not last_name:
                        full_name = str(row.get('name', row.get('student_name', ''))).strip()
                        if full_name:
                            name_parts = full_name.split(' ', 1)
                            first_name = name_parts[0]
                            last_name = name_parts[1] if len(name_parts) > 1 else ''
                    
                    # Extract marks with multiple fallback options
                    marks_obtained = row.get('marks', row.get('score', row.get('marks_obtained', 0)))
                    
                    # Validation
                    if not student_roll_number or not first_name:
                        errors.append(f"Row {index + 1}: Missing student ID or name")
                        continue
                    
                    if pd.isna(marks_obtained) or marks_obtained == '':
                        errors.append(f"Row {index + 1}: Missing marks for student {student_roll_number}")
                        continue
                    
                    # Find or create student
                    student = Student.query.filter_by(student_roll_number=student_roll_number).first()
                    if not student:
                        # Create new student
                        student = Student(
                            first_name=first_name,
                            last_name=last_name,
                            student_roll_number=student_roll_number
                        )
                        db.session.add(student)
                        db.session.flush()  # Get the ID
                        students_processed += 1
                        logger.info(f"Created new student: {student_roll_number} - {first_name} {last_name}")
                    else:
                        # Update existing student info if needed
                        updated = False
                        if student.first_name != first_name:
                            student.first_name = first_name
                            updated = True
                        if student.last_name != last_name:
                            student.last_name = last_name
                            updated = True
                        
                        if updated:
                            students_updated += 1
                            logger.info(f"Updated student info: {student_roll_number}")
                    
                    # Check for existing performance record (for recurring assessments)
                    existing_record = None
                    if is_recurring:
                        existing_record = PerformanceRecord.query.filter_by(
                            student_id=student.id,
                            assessment_id=assessment.id
                        ).first()
                    
                    if existing_record:
                        # Update existing record
                        existing_record.marks_obtained = float(marks_obtained)
                        existing_record.raw_data_from_excel = row.to_dict()
                        records_updated += 1
                        logger.info(f"Updated performance record for student {student_roll_number}")
                    else:
                        # Create new performance record
                        performance_record = PerformanceRecord(
                            marks_obtained=float(marks_obtained),
                            raw_data_from_excel=row.to_dict(),
                            student_id=student.id,
                            assessment_id=assessment.id
                        )
                        db.session.add(performance_record)
                        records_created += 1
                        logger.info(f"Created performance record for student {student_roll_number}: {marks_obtained} marks")
                    
                except ValueError as ve:
                    error_msg = f"Row {index + 1}: Invalid data format - {str(ve)}"
                    errors.append(error_msg)
                    logger.warning(error_msg)
                    continue
                except Exception as row_error:
                    error_msg = f"Row {index + 1}: {str(row_error)}"
                    errors.append(error_msg)
                    logger.warning(error_msg)
                    continue
            
            # Commit all changes
            db.session.commit()
            logger.info(f"Successfully processed file. Students: {students_processed}, Records: {records_created}")
            
            # Clean up uploaded file
            try:
                os.remove(file_path)
                logger.info("Temporary file cleaned up")
            except Exception as cleanup_error:
                logger.warning(f"Could not clean up temporary file: {str(cleanup_error)}")
            
            return jsonify({
                'success': True,
                'message': 'File processed successfully',
                'data': {
                    'subject_name': subject_name,
                    'assessment_name': assessment_name,
                    'is_recurring': is_recurring,
                    'students_processed': students_processed,
                    'students_updated': students_updated,
                    'records_created': records_created,
                    'records_updated': records_updated,
                    'total_rows': len(df),
                    'errors': errors[:10]  # Limit errors to first 10
                }
            }), 200
            
        except Exception as processing_error:
            # Rollback database changes
            db.session.rollback()
            
            # Clean up uploaded file
            try:
                os.remove(file_path)
            except:
                pass
            
            logger.error(f"Error processing Excel file: {str(processing_error)}")
            return jsonify({
                'success': False,
                'error': f'Error processing Excel file: {str(processing_error)}'
            }), 500
            
    except Exception as e:
        logger.error(f"Unexpected error in upload endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }), 500