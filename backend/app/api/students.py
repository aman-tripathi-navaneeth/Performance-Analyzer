from flask import Blueprint, request, jsonify
from app.models import db, Student, PerformanceRecord, Assessment, Subject
from sqlalchemy import func, or_, desc
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

students_bp = Blueprint('students', __name__)

@students_bp.route('', methods=['GET'])
def search_students():
    """
    Search students endpoint
    GET /api/v1/students?search={query}
    Returns JSON array of matching students based on name or roll number
    """
    try:
        # Get search query from parameters
        search_query = request.args.get('search', '').strip()
        year_filter = request.args.get('year', '').strip()
        section_filter = request.args.get('section', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        logger.info(f"Student search request: query='{search_query}', year='{year_filter}', section='{section_filter}', page={page}, per_page={per_page}")
        
        # Build base query - join with subjects to filter by year/section
        if year_filter or section_filter:
            # Join with performance records, assessments, and subjects to filter by year/section
            query = db.session.query(Student).join(
                PerformanceRecord, Student.id == PerformanceRecord.student_id
            ).join(
                Assessment, PerformanceRecord.assessment_id == Assessment.id
            ).join(
                Subject, Assessment.subject_id == Subject.id
            )
            
            # Apply year filter
            if year_filter:
                try:
                    year_int = int(year_filter)
                    query = query.filter(Subject.year == year_int)
                except ValueError:
                    pass
            
            # Apply section filter
            if section_filter:
                query = query.filter(Subject.section == section_filter)
            
            # Make sure we get distinct students
            query = query.distinct()
        else:
            query = db.session.query(Student)
        
        # Apply search filter if provided
        if search_query:
            # Use LIKE filter on name and roll number
            search_pattern = f"%{search_query}%"
            query = query.filter(
                or_(
                    Student.first_name.ilike(search_pattern),
                    Student.last_name.ilike(search_pattern),
                    Student.student_roll_number.ilike(search_pattern),
                    func.concat(Student.first_name, ' ', Student.last_name).ilike(search_pattern)
                )
            )
        
        # Order by name
        query = query.order_by(Student.first_name, Student.last_name)
        
        # Apply pagination
        paginated_students = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Get student performance data for each student
        students_data = []
        for student in paginated_students.items:
            # Get student's performance summary
            performance_summary = db.session.query(
                func.count(PerformanceRecord.id).label('total_assessments'),
                func.avg(PerformanceRecord.marks_obtained * 100.0 / Assessment.max_marks).label('avg_percentage'),
                func.count(func.distinct(Assessment.subject_id)).label('subjects_count')
            ).join(
                Assessment, PerformanceRecord.assessment_id == Assessment.id
            ).filter(
                PerformanceRecord.student_id == student.id
            ).first()
            
            # Get recent assessments
            recent_assessments = db.session.query(
                Assessment.assessment_name,
                Assessment.assessment_date,
                Subject.subject_name,
                PerformanceRecord.marks_obtained,
                Assessment.max_marks
            ).join(
                Assessment, PerformanceRecord.assessment_id == Assessment.id
            ).join(
                Subject, Assessment.subject_id == Subject.id
            ).filter(
                PerformanceRecord.student_id == student.id
            ).order_by(
                desc(Assessment.assessment_date)
            ).limit(3).all()
            
            recent_data = []
            for assessment in recent_assessments:
                percentage = (assessment.marks_obtained / assessment.max_marks * 100) if assessment.max_marks > 0 else 0
                recent_data.append({
                    'assessment_name': assessment.assessment_name,
                    'subject_name': assessment.subject_name,
                    'assessment_date': assessment.assessment_date.isoformat() if assessment.assessment_date else None,
                    'marks_obtained': assessment.marks_obtained,
                    'max_marks': assessment.max_marks,
                    'percentage': round(percentage, 2)
                })
            
            # Get student's year and section from their subjects
            student_year_section = db.session.query(
                Subject.year,
                Subject.section
            ).join(
                Assessment, Subject.id == Assessment.subject_id
            ).join(
                PerformanceRecord, Assessment.id == PerformanceRecord.assessment_id
            ).filter(
                PerformanceRecord.student_id == student.id,
                Subject.year.isnot(None),
                Subject.section.isnot(None)
            ).first()
            
            # Prepare student data
            avg_percentage = performance_summary.avg_percentage or 0
            student_data = {
                'id': str(student.id),
                'student_roll_number': student.student_roll_number,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'full_name': f"{student.first_name} {student.last_name}",
                'year': student_year_section.year if student_year_section else None,
                'section': student_year_section.section if student_year_section else None,
                'created_at': student.created_at.isoformat() if student.created_at else None,
                'performance_summary': {
                    'total_assessments': performance_summary.total_assessments or 0,
                    'average_percentage': round(avg_percentage, 2),
                    'subjects_count': performance_summary.subjects_count or 0,
                    'grade': get_grade_from_percentage(avg_percentage)
                },
                'recent_assessments': recent_data
            }
            
            students_data.append(student_data)
        
        # Prepare pagination info
        pagination_info = {
            'page': paginated_students.page,
            'per_page': paginated_students.per_page,
            'total': paginated_students.total,
            'pages': paginated_students.pages,
            'has_next': paginated_students.has_next,
            'has_prev': paginated_students.has_prev
        }
        
        logger.info(f"Found {len(students_data)} students matching query '{search_query}'")
        
        return jsonify({
            'success': True,
            'data': {
                'students': students_data,
                'pagination': pagination_info,
                'search_query': search_query
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching students: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error searching students: {str(e)}'
        }), 500

@students_bp.route('/<student_id>', methods=['GET'])
def get_student_detail(student_id):
    """
    Get detailed student information
    GET /api/v1/students/{student_id}
    Returns detailed student profile with all performance data
    """
    try:
        logger.info(f"Fetching detailed data for student: {student_id}")
        
        # Find student by ID or roll number
        student = None
        try:
            # Try to find by UUID first
            student = Student.query.filter_by(id=student_id).first()
        except:
            pass
        
        if not student:
            # Try to find by roll number
            student = Student.query.filter_by(student_roll_number=student_id).first()
        
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        # Get all performance records for this student
        performance_records = db.session.query(
            PerformanceRecord.marks_obtained,
            PerformanceRecord.created_at,
            Assessment.assessment_name,
            Assessment.assessment_date,
            Assessment.max_marks,
            Subject.subject_name
        ).join(
            Assessment, PerformanceRecord.assessment_id == Assessment.id
        ).join(
            Subject, Assessment.subject_id == Subject.id
        ).filter(
            PerformanceRecord.student_id == student.id
        ).order_by(
            desc(Assessment.assessment_date)
        ).all()
        
        # Organize performance data by subject
        subjects_performance = {}
        all_percentages = []
        
        for record in performance_records:
            subject_name = record.subject_name
            percentage = (record.marks_obtained / record.max_marks * 100) if record.max_marks > 0 else 0
            all_percentages.append(percentage)
            
            if subject_name not in subjects_performance:
                subjects_performance[subject_name] = {
                    'assessments': [],
                    'average_percentage': 0,
                    'total_assessments': 0
                }
            
            subjects_performance[subject_name]['assessments'].append({
                'assessment_name': record.assessment_name,
                'assessment_date': record.assessment_date.isoformat() if record.assessment_date else None,
                'marks_obtained': record.marks_obtained,
                'max_marks': record.max_marks,
                'percentage': round(percentage, 2),
                'grade': get_grade_from_percentage(percentage),
                'created_at': record.created_at.isoformat() if record.created_at else None
            })
        
        # Calculate averages for each subject
        for subject_name, subject_data in subjects_performance.items():
            assessments = subject_data['assessments']
            if assessments:
                avg_percentage = sum(a['percentage'] for a in assessments) / len(assessments)
                subject_data['average_percentage'] = round(avg_percentage, 2)
                subject_data['total_assessments'] = len(assessments)
                subject_data['grade'] = get_grade_from_percentage(avg_percentage)
        
        # Calculate overall performance
        overall_average = sum(all_percentages) / len(all_percentages) if all_percentages else 0
        
        # Prepare detailed student data
        student_detail = {
            'id': str(student.id),
            'student_roll_number': student.student_roll_number,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'full_name': f"{student.first_name} {student.last_name}",
            'created_at': student.created_at.isoformat() if student.created_at else None,
            'overall_performance': {
                'average_percentage': round(overall_average, 2),
                'grade': get_grade_from_percentage(overall_average),
                'total_assessments': len(performance_records),
                'subjects_count': len(subjects_performance)
            },
            'subjects_performance': subjects_performance,
            'performance_trend': [
                {
                    'assessment_name': record.assessment_name,
                    'subject_name': record.subject_name,
                    'percentage': round((record.marks_obtained / record.max_marks * 100), 2) if record.max_marks > 0 else 0,
                    'assessment_date': record.assessment_date.isoformat() if record.assessment_date else None
                }
                for record in performance_records
            ]
        }
        
        logger.info(f"Successfully retrieved detailed data for student {student.student_roll_number}")
        
        return jsonify({
            'success': True,
            'data': student_detail
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching student detail: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error fetching student detail: {str(e)}'
        }), 500

@students_bp.route('/<uuid:student_id>/performance', methods=['GET'])
def get_student_performance(student_id):
    """
    Get detailed student performance data
    GET /api/v1/student/{student_id}/performance
    Returns complete structured JSON for student's profile page
    """
    try:
        logger.info(f"Fetching performance data for student ID: {student_id}")
        
        # Find student by UUID
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        # Get all performance records with full details
        performance_query = db.session.query(
            PerformanceRecord.id,
            PerformanceRecord.marks_obtained,
            PerformanceRecord.raw_data_from_excel,
            PerformanceRecord.created_at,
            Assessment.id.label('assessment_id'),
            Assessment.assessment_name,
            Assessment.assessment_date,
            Assessment.max_marks,
            Subject.id.label('subject_id'),
            Subject.subject_name
        ).join(
            Assessment, PerformanceRecord.assessment_id == Assessment.id
        ).join(
            Subject, Assessment.subject_id == Subject.id
        ).filter(
            PerformanceRecord.student_id == student_id
        ).order_by(
            Subject.subject_name,
            desc(Assessment.assessment_date)
        ).all()
        
        if not performance_query:
            # Return student info even if no performance records
            return jsonify({
                'success': True,
                'data': {
                    'student_info': {
                        'id': str(student.id),
                        'student_roll_number': student.student_roll_number,
                        'first_name': student.first_name,
                        'last_name': student.last_name,
                        'full_name': f"{student.first_name} {student.last_name}",
                        'created_at': student.created_at.isoformat() if student.created_at else None
                    },
                    'performance_summary': {
                        'total_assessments': 0,
                        'overall_average': 0,
                        'overall_grade': 'N/A',
                        'subjects_count': 0
                    },
                    'subjects_performance': {},
                    'assessment_timeline': [],
                    'performance_trends': {},
                    'grade_breakdown': {}
                }
            }), 200
        
        # Organize data by subject
        subjects_performance = {}
        all_assessments = []
        all_percentages = []
        grade_counts = {'A+': 0, 'A': 0, 'B+': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        
        for record in performance_query:
            subject_name = record.subject_name
            percentage = (record.marks_obtained / record.max_marks * 100) if record.max_marks > 0 else 0
            grade = get_grade_from_percentage(percentage)
            
            all_percentages.append(percentage)
            grade_counts[grade] += 1
            
            # Initialize subject if not exists
            if subject_name not in subjects_performance:
                subjects_performance[subject_name] = {
                    'subject_id': str(record.subject_id),
                    'subject_name': subject_name,
                    'assessments': [],
                    'statistics': {
                        'total_assessments': 0,
                        'average_percentage': 0,
                        'highest_percentage': 0,
                        'lowest_percentage': 100,
                        'grade': 'N/A',
                        'improvement_trend': 'stable'
                    }
                }
            
            # Add assessment to subject
            assessment_data = {
                'assessment_id': str(record.assessment_id),
                'assessment_name': record.assessment_name,
                'assessment_date': record.assessment_date.isoformat() if record.assessment_date else None,
                'marks_obtained': record.marks_obtained,
                'max_marks': record.max_marks,
                'percentage': round(percentage, 2),
                'grade': grade,
                'created_at': record.created_at.isoformat() if record.created_at else None,
                'raw_data': record.raw_data_from_excel
            }
            
            subjects_performance[subject_name]['assessments'].append(assessment_data)
            
            # Add to timeline
            all_assessments.append({
                'assessment_name': record.assessment_name,
                'subject_name': subject_name,
                'assessment_date': record.assessment_date.isoformat() if record.assessment_date else None,
                'percentage': round(percentage, 2),
                'grade': grade,
                'marks_obtained': record.marks_obtained,
                'max_marks': record.max_marks
            })
        
        # Calculate statistics for each subject
        for subject_name, subject_data in subjects_performance.items():
            assessments = subject_data['assessments']
            percentages = [a['percentage'] for a in assessments]
            
            if percentages:
                avg_percentage = sum(percentages) / len(percentages)
                subject_data['statistics'].update({
                    'total_assessments': len(assessments),
                    'average_percentage': round(avg_percentage, 2),
                    'highest_percentage': round(max(percentages), 2),
                    'lowest_percentage': round(min(percentages), 2),
                    'grade': get_grade_from_percentage(avg_percentage)
                })
                
                # Calculate improvement trend (compare first half vs second half)
                if len(percentages) >= 4:
                    mid_point = len(percentages) // 2
                    first_half_avg = sum(percentages[:mid_point]) / mid_point
                    second_half_avg = sum(percentages[mid_point:]) / (len(percentages) - mid_point)
                    
                    if second_half_avg > first_half_avg + 5:
                        subject_data['statistics']['improvement_trend'] = 'improving'
                    elif second_half_avg < first_half_avg - 5:
                        subject_data['statistics']['improvement_trend'] = 'declining'
                    else:
                        subject_data['statistics']['improvement_trend'] = 'stable'
        
        # Sort timeline by date (most recent first)
        all_assessments.sort(key=lambda x: x['assessment_date'] or '', reverse=True)
        
        # Calculate performance trends for charts
        performance_trends = {}
        for subject_name, subject_data in subjects_performance.items():
            assessments = sorted(subject_data['assessments'], 
                               key=lambda x: x['assessment_date'] or '', reverse=False)
            
            performance_trends[subject_name] = {
                'labels': [a['assessment_name'] for a in assessments],
                'data': [a['percentage'] for a in assessments],
                'dates': [a['assessment_date'] for a in assessments]
            }
        
        # Calculate overall statistics
        overall_average = sum(all_percentages) / len(all_percentages) if all_percentages else 0
        
        # Prepare complete response
        student_performance_data = {
            'student_info': {
                'id': str(student.id),
                'student_roll_number': student.student_roll_number,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'full_name': f"{student.first_name} {student.last_name}",
                'created_at': student.created_at.isoformat() if student.created_at else None
            },
            'performance_summary': {
                'total_assessments': len(all_assessments),
                'overall_average': round(overall_average, 2),
                'overall_grade': get_grade_from_percentage(overall_average),
                'subjects_count': len(subjects_performance),
                'highest_score': round(max(all_percentages), 2) if all_percentages else 0,
                'lowest_score': round(min(all_percentages), 2) if all_percentages else 0
            },
            'subjects_performance': subjects_performance,
            'assessment_timeline': all_assessments,
            'performance_trends': performance_trends,
            'grade_breakdown': grade_counts,
            'insights': {
                'strongest_subject': max(subjects_performance.items(), 
                                       key=lambda x: x[1]['statistics']['average_percentage'])[0] if subjects_performance else None,
                'weakest_subject': min(subjects_performance.items(), 
                                     key=lambda x: x[1]['statistics']['average_percentage'])[0] if subjects_performance else None,
                'most_improved': next((name for name, data in subjects_performance.items() 
                                     if data['statistics']['improvement_trend'] == 'improving'), None),
                'needs_attention': [name for name, data in subjects_performance.items() 
                                  if data['statistics']['average_percentage'] < 60]
            }
        }
        
        logger.info(f"Successfully retrieved performance data for student {student.student_roll_number}: {len(all_assessments)} assessments across {len(subjects_performance)} subjects")
        
        return jsonify({
            'success': True,
            'data': student_performance_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching student performance: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error fetching student performance: {str(e)}'
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