from flask import Blueprint, request, jsonify
import sqlite3
from app.models import DatabaseManager, Subject
from app.services import calculate_percentage, get_grade
import json

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/class-performance', methods=['GET'])
def get_class_performance():
    """Get overall class performance across all subjects"""
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Get class performance by subject
        cursor.execute('''
            SELECT s.name as subject_name, s.subject_type,
                   AVG(pd.score) as avg_score,
                   AVG(pd.max_score) as avg_max_score,
                   COUNT(DISTINCT pd.student_id) as student_count,
                   COUNT(pd.id) as total_records
            FROM performance_data pd
            JOIN subjects s ON pd.subject_id = s.id
            GROUP BY s.id, s.name, s.subject_type
            ORDER BY s.name
        ''')
        
        class_data = cursor.fetchall()
        conn.close()
        
        subjects_performance = []
        for data in class_data:
            avg_percentage = calculate_percentage(data[2], data[3])
            subjects_performance.append({
                'subject_name': data[0],
                'subject_type': data[1],
                'average_score': round(data[2], 2),
                'average_percentage': round(avg_percentage, 2),
                'grade': get_grade(avg_percentage),
                'student_count': data[4],
                'total_records': data[5]
            })
        
        # Calculate overall class average
        overall_avg = 0
        if subjects_performance:
            overall_avg = sum(s['average_percentage'] for s in subjects_performance) / len(subjects_performance)
        
        return jsonify({
            'subjects_performance': subjects_performance,
            'overall_class_average': round(overall_avg, 2),
            'overall_grade': get_grade(overall_avg)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/subject-performance/<int:subject_id>', methods=['GET'])
def get_subject_performance(subject_id):
    """Get detailed performance for a specific subject"""
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Get subject info
        cursor.execute('SELECT name, subject_type FROM subjects WHERE id = ?', (subject_id,))
        subject_info = cursor.fetchone()
        
        if not subject_info:
            return jsonify({'error': 'Subject not found'}), 404
        
        # Get all performance data for this subject
        cursor.execute('''
            SELECT pd.student_id, s.name as student_name,
                   pd.data_type, pd.score, pd.max_score, pd.week_number
            FROM performance_data pd
            JOIN students s ON pd.student_id = s.student_id
            WHERE pd.subject_id = ?
            ORDER BY s.name, pd.week_number
        ''', (subject_id,))
        
        performance_data = cursor.fetchall()
        conn.close()
        
        # Organize data by student
        students_data = {}
        for data in performance_data:
            student_id = data[0]
            if student_id not in students_data:
                students_data[student_id] = {
                    'student_name': data[1],
                    'scores': [],
                    'average_percentage': 0
                }
            
            percentage = calculate_percentage(data[3], data[4])
            students_data[student_id]['scores'].append({
                'data_type': data[2],
                'score': data[3],
                'max_score': data[4],
                'percentage': percentage,
                'week_number': data[5]
            })
        
        # Calculate averages
        for student_id, student_data in students_data.items():
            if student_data['scores']:
                avg_percentage = sum(score['percentage'] for score in student_data['scores']) / len(student_data['scores'])
                student_data['average_percentage'] = round(avg_percentage, 2)
                student_data['grade'] = get_grade(avg_percentage)
        
        return jsonify({
            'subject_name': subject_info[0],
            'subject_type': subject_info[1],
            'students_performance': students_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/trends', methods=['GET'])
def get_performance_trends():
    """Get performance trends over time (especially for CRT data)"""
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Get weekly CRT trends
        cursor.execute('''
            SELECT s.name as subject_name, pd.week_number,
                   AVG(pd.score) as avg_score,
                   AVG(pd.max_score) as avg_max_score,
                   COUNT(pd.student_id) as student_count
            FROM performance_data pd
            JOIN subjects s ON pd.subject_id = s.id
            WHERE s.subject_type = 'crt' AND pd.week_number IS NOT NULL
            GROUP BY s.id, pd.week_number
            ORDER BY s.name, pd.week_number
        ''')
        
        trends_data = cursor.fetchall()
        conn.close()
        
        # Organize trends by subject
        subjects_trends = {}
        for data in trends_data:
            subject_name = data[0]
            if subject_name not in subjects_trends:
                subjects_trends[subject_name] = []
            
            avg_percentage = calculate_percentage(data[2], data[3])
            subjects_trends[subject_name].append({
                'week': data[1],
                'average_score': round(data[2], 2),
                'average_percentage': round(avg_percentage, 2),
                'student_count': data[4]
            })
        
        return jsonify({'trends': subjects_trends}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get overall system statistics"""
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Get basic counts
        cursor.execute('SELECT COUNT(*) FROM students')
        total_students = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM subjects')
        total_subjects = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM performance_data')
        total_records = cursor.fetchone()[0]
        
        # Get grade distribution
        cursor.execute('''
            SELECT pd.student_id, AVG(pd.score * 100.0 / pd.max_score) as avg_percentage
            FROM performance_data pd
            GROUP BY pd.student_id
        ''')
        
        student_averages = cursor.fetchall()
        conn.close()
        
        # Calculate grade distribution
        grade_distribution = {'A+': 0, 'A': 0, 'B+': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for avg_data in student_averages:
            grade = get_grade(avg_data[1])
            grade_distribution[grade] += 1
        
        return jsonify({
            'total_students': total_students,
            'total_subjects': total_subjects,
            'total_records': total_records,
            'grade_distribution': grade_distribution
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500