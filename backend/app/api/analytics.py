from flask import Blueprint, request, jsonify
from app.models import db, Student, Subject, Assessment, PerformanceRecord
from sqlalchemy import func, desc
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/class/overview', methods=['GET'])
def get_class_overview():
    """
    Get class overview data for the main dashboard
    GET /api/v1/class/overview
    Returns aggregated data structured for dashboard charts
    """
    try:
        logger.info("Fetching class overview data")
        
        # 1. Overall Statistics
        total_students = db.session.query(Student).count()
        total_subjects = db.session.query(Subject).count()
        total_assessments = db.session.query(Assessment).count()
        total_records = db.session.query(PerformanceRecord).count()
        
        # 2. Average Scores per Subject
        subject_averages = db.session.query(
            Subject.subject_name,
            func.avg(PerformanceRecord.marks_obtained).label('avg_marks'),
            func.avg(Assessment.max_marks).label('avg_max_marks'),
            func.count(PerformanceRecord.id).label('total_records'),
            func.count(func.distinct(PerformanceRecord.student_id)).label('unique_students')
        ).join(
            Assessment, Subject.id == Assessment.subject_id
        ).join(
            PerformanceRecord, Assessment.id == PerformanceRecord.assessment_id
        ).group_by(
            Subject.id, Subject.subject_name
        ).all()
        
        # Process subject data for charts
        subjects_data = []
        for record in subject_averages:
            avg_percentage = (record.avg_marks / record.avg_max_marks * 100) if record.avg_max_marks > 0 else 0
            subjects_data.append({
                'subject_name': record.subject_name,
                'average_marks': round(record.avg_marks, 2),
                'average_percentage': round(avg_percentage, 2),
                'total_records': record.total_records,
                'unique_students': record.unique_students,
                'grade': get_grade_from_percentage(avg_percentage)
            })
        
        # Sort by average percentage descending
        subjects_data.sort(key=lambda x: x['average_percentage'], reverse=True)
        
        # 3. Year Distribution (based on subjects with year information)
        year_distribution = {}
        
        # Get year distribution from subjects
        year_counts = db.session.query(
            Subject.year,
            func.count(func.distinct(PerformanceRecord.student_id)).label('student_count')
        ).join(
            Assessment, Subject.id == Assessment.subject_id
        ).join(
            PerformanceRecord, Assessment.id == PerformanceRecord.assessment_id
        ).filter(
            Subject.year.isnot(None)
        ).group_by(
            Subject.year
        ).all()
        
        # Initialize year counts
        year_distribution = {
            '1st Year': 0,
            '2nd Year': 0,
            '3rd Year': 0,
            '4th Year': 0
        }
        
        # Map year numbers to year labels
        year_mapping = {
            1: '1st Year',
            2: '2nd Year', 
            3: '3rd Year',
            4: '4th Year'
        }
        
        for year_count in year_counts:
            if year_count.year in year_mapping:
                year_distribution[year_mapping[year_count.year]] = year_count.student_count
        
        # Also calculate grade distribution for backward compatibility
        grade_distribution = {}
        all_student_averages = db.session.query(
            Student.student_roll_number,
            func.avg(PerformanceRecord.marks_obtained * 100.0 / Assessment.max_marks).label('avg_percentage')
        ).join(
            PerformanceRecord, Student.id == PerformanceRecord.student_id
        ).join(
            Assessment, PerformanceRecord.assessment_id == Assessment.id
        ).group_by(
            Student.id, Student.student_roll_number
        ).all()
        
        # Initialize grade counts
        grades = ['A+', 'A', 'B+', 'B', 'C', 'D', 'F']
        grade_distribution = {grade: 0 for grade in grades}
        
        for student_avg in all_student_averages:
            grade = get_grade_from_percentage(student_avg.avg_percentage)
            grade_distribution[grade] += 1
        
        # 4. Recent Assessment Performance
        recent_assessments = db.session.query(
            Assessment.assessment_name,
            Assessment.assessment_date,
            Subject.subject_name,
            func.avg(PerformanceRecord.marks_obtained).label('avg_marks'),
            Assessment.max_marks,
            func.count(PerformanceRecord.id).label('submissions')
        ).join(
            Subject, Assessment.subject_id == Subject.id
        ).join(
            PerformanceRecord, Assessment.id == PerformanceRecord.assessment_id
        ).group_by(
            Assessment.id, Assessment.assessment_name, Assessment.assessment_date,
            Subject.subject_name, Assessment.max_marks
        ).order_by(
            desc(Assessment.assessment_date)
        ).limit(10).all()
        
        recent_data = []
        for assessment in recent_assessments:
            avg_percentage = (assessment.avg_marks / assessment.max_marks * 100) if assessment.max_marks > 0 else 0
            recent_data.append({
                'assessment_name': assessment.assessment_name,
                'subject_name': assessment.subject_name,
                'assessment_date': assessment.assessment_date.isoformat() if assessment.assessment_date else None,
                'average_marks': round(assessment.avg_marks, 2),
                'max_marks': assessment.max_marks,
                'average_percentage': round(avg_percentage, 2),
                'submissions': assessment.submissions,
                'grade': get_grade_from_percentage(avg_percentage)
            })
        
        # 5. Top and Bottom Performing Students
        student_performance = db.session.query(
            Student.student_roll_number,
            Student.first_name,
            Student.last_name,
            func.avg(PerformanceRecord.marks_obtained * 100.0 / Assessment.max_marks).label('avg_percentage'),
            func.count(PerformanceRecord.id).label('total_assessments')
        ).join(
            PerformanceRecord, Student.id == PerformanceRecord.student_id
        ).join(
            Assessment, PerformanceRecord.assessment_id == Assessment.id
        ).group_by(
            Student.id, Student.student_roll_number, Student.first_name, Student.last_name
        ).having(
            func.count(PerformanceRecord.id) >= 3  # At least 3 assessments
        ).order_by(
            desc('avg_percentage')
        ).all()
        
        top_performers = []
        bottom_performers = []
        
        for i, student in enumerate(student_performance[:5]):  # Top 5
            top_performers.append({
                'rank': i + 1,
                'student_roll_number': student.student_roll_number,
                'full_name': f"{student.first_name} {student.last_name}",
                'average_percentage': round(student.avg_percentage, 2),
                'total_assessments': student.total_assessments,
                'grade': get_grade_from_percentage(student.avg_percentage)
            })
        
        for i, student in enumerate(student_performance[-5:]):  # Bottom 5
            bottom_performers.append({
                'rank': len(student_performance) - 4 + i,
                'student_roll_number': student.student_roll_number,
                'full_name': f"{student.first_name} {student.last_name}",
                'average_percentage': round(student.avg_percentage, 2),
                'total_assessments': student.total_assessments,
                'grade': get_grade_from_percentage(student.avg_percentage)
            })
        
        # 6. Calculate overall class average
        overall_class_average = 0
        if subjects_data:
            overall_class_average = sum(subject['average_percentage'] for subject in subjects_data) / len(subjects_data)
        
        # Prepare response data
        overview_data = {
            'statistics': {
                'total_students': total_students,
                'total_subjects': total_subjects,
                'total_assessments': total_assessments,
                'total_records': total_records,
                'overall_class_average': round(overall_class_average, 2),
                'overall_grade': get_grade_from_percentage(overall_class_average)
            },
            'subjects_performance': subjects_data,
            'grade_distribution': grade_distribution,
            'year_distribution': year_distribution,
            'recent_assessments': recent_data,
            'top_performers': top_performers,
            'bottom_performers': bottom_performers,
            'charts_data': {
                'subject_averages': {
                    'labels': [subject['subject_name'] for subject in subjects_data],
                    'data': [subject['average_percentage'] for subject in subjects_data]
                },
                'grade_distribution': {
                    'labels': list(grade_distribution.keys()),
                    'data': list(grade_distribution.values())
                }
            }
        }
        
        logger.info(f"Successfully retrieved class overview data for {total_students} students")
        
        return jsonify({
            'success': True,
            'data': overview_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching class overview: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error fetching class overview: {str(e)}'
        }), 500

def get_grade_from_percentage(percentage):
    """Convert percentage to letter grade"""
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