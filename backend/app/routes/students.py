from flask import Blueprint, request, jsonify
from app.models import Student, PerformanceData
from app.services import calculate_percentage, get_grade

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['GET'])
def get_all_students():
    """Get all students"""
    try:
        students = Student.get_all()
        return jsonify({'students': students}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/<student_id>', methods=['GET'])
def get_student_profile(student_id):
    """Get individual student performance profile"""
    try:
        # Get student info
        student = Student.find_by_id(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Get performance data
        performance_data = PerformanceData.get_student_performance(student_id)
        
        # Organize data by subject
        subjects_performance = {}
        for data in performance_data:
            subject_name = data['subject_name']
            if subject_name not in subjects_performance:
                subjects_performance[subject_name] = {
                    'subject_type': data['subject_type'],
                    'scores': [],
                    'average_percentage': 0,
                    'grade': 'N/A'
                }
            
            percentage = calculate_percentage(data['score'], data['max_score'])
            subjects_performance[subject_name]['scores'].append({
                'data_type': data['data_type'],
                'score': data['score'],
                'max_score': data['max_score'],
                'percentage': percentage,
                'week_number': data['week_number'],
                'upload_date': data['upload_date']
            })
        
        # Calculate averages and grades
        for subject_name, subject_data in subjects_performance.items():
            if subject_data['scores']:
                avg_percentage = sum(score['percentage'] for score in subject_data['scores']) / len(subject_data['scores'])
                subject_data['average_percentage'] = round(avg_percentage, 2)
                subject_data['grade'] = get_grade(avg_percentage)
        
        # Calculate overall performance
        overall_percentage = 0
        if subjects_performance:
            overall_percentage = sum(data['average_percentage'] for data in subjects_performance.values()) / len(subjects_performance)
        
        return jsonify({
            'student': student,
            'subjects_performance': subjects_performance,
            'overall_percentage': round(overall_percentage, 2),
            'overall_grade': get_grade(overall_percentage)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@students_bp.route('/search', methods=['GET'])
def search_students():
    """Search students by name or ID"""
    try:
        query = request.args.get('q', '').strip().lower()
        if not query:
            return jsonify({'students': []}), 200
        
        all_students = Student.get_all()
        filtered_students = [
            student for student in all_students
            if query in student['name'].lower() or query in student['student_id'].lower()
        ]
        
        return jsonify({'students': filtered_students}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500