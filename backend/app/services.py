from app.models import DatabaseManager, PerformanceData
from app.utils import calculate_percentage, get_grade
import sqlite3

class PerformanceAnalysisService:
    """Service for advanced performance analysis and data merging"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def merge_crt_data(self, student_id, subject_id, new_week_data):
        """Merge new CRT week data with existing data"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Check if data for this week already exists
            cursor.execute('''
                SELECT id FROM performance_data 
                WHERE student_id = ? AND subject_id = ? AND week_number = ?
            ''', (student_id, subject_id, new_week_data['week_number']))
            
            existing_record = cursor.fetchone()
            
            if existing_record:
                # Update existing record
                cursor.execute('''
                    UPDATE performance_data 
                    SET score = ?, max_score = ?, upload_date = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (new_week_data['score'], new_week_data['max_score'], existing_record[0]))
                action = 'updated'
            else:
                # Insert new record
                perf_data = PerformanceData(
                    student_id=student_id,
                    subject_id=subject_id,
                    data_type='CRT Score',
                    score=new_week_data['score'],
                    max_score=new_week_data['max_score'],
                    week_number=new_week_data['week_number']
                )
                perf_data.save()
                action = 'added'
            
            conn.commit()
            conn.close()
            return action
            
        except Exception as e:
            raise Exception(f"Error merging CRT data: {str(e)}")
    
    def get_student_progress_over_time(self, student_id, subject_id):
        """Get student's progress over time for a specific subject"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT week_number, score, max_score, upload_date
                FROM performance_data
                WHERE student_id = ? AND subject_id = ?
                ORDER BY week_number ASC
            ''', (student_id, subject_id))
            
            data = cursor.fetchall()
            conn.close()
            
            progress = []
            for record in data:
                percentage = calculate_percentage(record[1], record[2])
                progress.append({
                    'week': record[0],
                    'score': record[1],
                    'max_score': record[2],
                    'percentage': round(percentage, 2),
                    'date': record[3]
                })
            
            return progress
            
        except Exception as e:
            raise Exception(f"Error getting student progress: {str(e)}")
    
    def get_class_comparison(self, subject_id):
        """Get class performance comparison for a subject"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT pd.student_id, s.name as student_name,
                       AVG(pd.score) as avg_score,
                       AVG(pd.max_score) as avg_max_score,
                       COUNT(pd.id) as total_assessments
                FROM performance_data pd
                JOIN students s ON pd.student_id = s.student_id
                WHERE pd.subject_id = ?
                GROUP BY pd.student_id, s.name
                ORDER BY avg_score DESC
            ''', (subject_id,))
            
            data = cursor.fetchall()
            conn.close()
            
            comparison = []
            for record in data:
                avg_percentage = calculate_percentage(record[2], record[3])
                comparison.append({
                    'student_id': record[0],
                    'student_name': record[1],
                    'average_score': round(record[2], 2),
                    'average_percentage': round(avg_percentage, 2),
                    'grade': get_grade(avg_percentage),
                    'total_assessments': record[4],
                    'rank': len(comparison) + 1
                })
            
            return comparison
            
        except Exception as e:
            raise Exception(f"Error getting class comparison: {str(e)}")
    
    def identify_struggling_students(self, threshold_percentage=50):
        """Identify students who are struggling (below threshold)"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT pd.student_id, s.name as student_name,
                       AVG(pd.score * 100.0 / pd.max_score) as avg_percentage,
                       COUNT(DISTINCT pd.subject_id) as subjects_count
                FROM performance_data pd
                JOIN students s ON pd.student_id = s.student_id
                GROUP BY pd.student_id, s.name
                HAVING avg_percentage < ?
                ORDER BY avg_percentage ASC
            ''', (threshold_percentage,))
            
            data = cursor.fetchall()
            conn.close()
            
            struggling_students = []
            for record in data:
                struggling_students.append({
                    'student_id': record[0],
                    'student_name': record[1],
                    'average_percentage': round(record[2], 2),
                    'subjects_count': record[3],
                    'grade': get_grade(record[2])
                })
            
            return struggling_students
            
        except Exception as e:
            raise Exception(f"Error identifying struggling students: {str(e)}")
    
    def get_subject_difficulty_analysis(self):
        """Analyze which subjects are most difficult based on class averages"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT s.name as subject_name, s.subject_type,
                       AVG(pd.score * 100.0 / pd.max_score) as avg_percentage,
                       COUNT(DISTINCT pd.student_id) as student_count,
                       MIN(pd.score * 100.0 / pd.max_score) as min_percentage,
                       MAX(pd.score * 100.0 / pd.max_score) as max_percentage
                FROM performance_data pd
                JOIN subjects s ON pd.subject_id = s.id
                GROUP BY s.id, s.name, s.subject_type
                ORDER BY avg_percentage ASC
            ''')
            
            data = cursor.fetchall()
            conn.close()
            
            difficulty_analysis = []
            for record in data:
                difficulty_level = 'Easy'
                if record[2] < 60:
                    difficulty_level = 'Hard'
                elif record[2] < 75:
                    difficulty_level = 'Medium'
                
                difficulty_analysis.append({
                    'subject_name': record[0],
                    'subject_type': record[1],
                    'average_percentage': round(record[2], 2),
                    'student_count': record[3],
                    'min_percentage': round(record[4], 2),
                    'max_percentage': round(record[5], 2),
                    'difficulty_level': difficulty_level,
                    'grade': get_grade(record[2])
                })
            
            return difficulty_analysis
            
        except Exception as e:
            raise Exception(f"Error analyzing subject difficulty: {str(e)}")