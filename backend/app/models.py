import sqlite3
import json
from datetime import datetime
from app.config import Config

class DatabaseManager:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Subjects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Performance data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                subject_id INTEGER NOT NULL,
                data_type TEXT NOT NULL,
                score REAL NOT NULL,
                max_score REAL NOT NULL,
                week_number INTEGER,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                FOREIGN KEY (subject_id) REFERENCES subjects (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
    
    def save(self):
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO students (student_id, name)
            VALUES (?, ?)
        ''', (self.student_id, self.name))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all():
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT student_id, name FROM students ORDER BY name')
        students = cursor.fetchall()
        conn.close()
        
        return [{'student_id': s[0], 'name': s[1]} for s in students]
    
    @staticmethod
    def find_by_id(student_id):
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT student_id, name FROM students WHERE student_id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()
        
        return {'student_id': student[0], 'name': student[1]} if student else None

class Subject:
    def __init__(self, name, subject_type):
        self.name = name
        self.subject_type = subject_type
    
    def save(self):
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO subjects (name, subject_type)
            VALUES (?, ?)
        ''', (self.name, self.subject_type))
        
        subject_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return subject_id
    
    @staticmethod
    def get_all():
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, subject_type FROM subjects')
        subjects = cursor.fetchall()
        conn.close()
        
        return [{'id': s[0], 'name': s[1], 'type': s[2]} for s in subjects]

class PerformanceData:
    def __init__(self, student_id, subject_id, data_type, score, max_score, week_number=None, metadata=None):
        self.student_id = student_id
        self.subject_id = subject_id
        self.data_type = data_type
        self.score = score
        self.max_score = max_score
        self.week_number = week_number
        self.metadata = json.dumps(metadata) if metadata else None
    
    def save(self):
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO performance_data 
            (student_id, subject_id, data_type, score, max_score, week_number, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.student_id, self.subject_id, self.data_type, 
              self.score, self.max_score, self.week_number, self.metadata))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_student_performance(student_id):
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT pd.*, s.name as subject_name, s.subject_type
            FROM performance_data pd
            JOIN subjects s ON pd.subject_id = s.id
            WHERE pd.student_id = ?
            ORDER BY pd.upload_date DESC
        ''', (student_id,))
        
        data = cursor.fetchall()
        conn.close()
        
        return [{'id': d[0], 'student_id': d[1], 'subject_id': d[2], 
                'data_type': d[3], 'score': d[4], 'max_score': d[5],
                'week_number': d[6], 'upload_date': d[7], 'metadata': d[8],
                'subject_name': d[9], 'subject_type': d[10]} for d in data]