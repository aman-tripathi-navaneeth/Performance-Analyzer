from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from app.services import allowed_file, process_excel_file
from app.models import Student, Subject, PerformanceData

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload and process Excel file with student performance data"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        subject_name = request.form.get('subject_name')
        subject_type = request.form.get('subject_type', 'regular')
        
        if not subject_name:
            return jsonify({'error': 'Subject name is required'}), 400
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only Excel files are allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the Excel file
        processed_data = process_excel_file(file_path, subject_name, subject_type)
        
        # Save subject
        subject = Subject(subject_name, subject_type)
        subject_id = subject.save()
        
        # Save students and performance data
        students_added = 0
        records_added = 0
        
        for data in processed_data:
            # Save student
            student = Student(data['student_id'], data['student_name'])
            student.save()
            students_added += 1
            
            # Save performance data
            perf_data = PerformanceData(
                student_id=data['student_id'],
                subject_id=subject_id,
                data_type=data['data_type'],
                score=data['score'],
                max_score=data['max_score'],
                week_number=data['week_number']
            )
            perf_data.save()
            records_added += 1
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return jsonify({
            'message': 'File processed successfully',
            'subject_name': subject_name,
            'subject_type': subject_type,
            'students_processed': len(set(d['student_id'] for d in processed_data)),
            'records_added': records_added
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@uploads_bp.route('/subjects', methods=['GET'])
def get_subjects():
    """Get all subjects"""
    try:
        subjects = Subject.get_all()
        return jsonify({'subjects': subjects}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500