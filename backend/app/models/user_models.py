import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from app.config import Config

class UserManager:
    def __init__(self):
        self.db_path = getattr(Config, 'DATABASE_PATH', 'performance_analyzer.db')
        self.init_user_tables()
    
    def init_user_tables(self):
        """Initialize user-related database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'teacher',
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                UNIQUE(email, role)
            )
        ''')
        
        # Sessions table for token management
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Sections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Teacher-Section assignments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teacher_sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                section_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (section_id) REFERENCES sections (id),
                UNIQUE(user_id, section_id)
            )
        ''')
        
        conn.commit()
        
        # Create default admin and teacher if they don't exist
        self._create_default_users(cursor, conn)
        
        conn.close()
    
    def _create_default_users(self, cursor, conn):
        """Create default admin and teacher users"""
        # Create admin if doesn't exist
        cursor.execute('SELECT id FROM users WHERE email = ? AND role = ?', ('aman@gmail.com', 'admin'))
        if not cursor.fetchone():
            admin_password_hash = self._hash_password('aman123')
            cursor.execute('''
                INSERT OR IGNORE INTO users (email, password_hash, name, role)
                VALUES (?, ?, ?, ?)
            ''', ('aman@gmail.com', admin_password_hash, 'Administrator', 'admin'))
        
        # Create teacher if doesn't exist  
        cursor.execute('SELECT id FROM users WHERE email = ? AND role = ?', ('aman@gmail.com', 'teacher'))
        if not cursor.fetchone():
            teacher_password_hash = self._hash_password('aman123')
            cursor.execute('''
                INSERT OR IGNORE INTO users (email, password_hash, name, role)
                VALUES (?, ?, ?, ?)
            ''', ('aman@gmail.com', teacher_password_hash, 'Teacher', 'teacher'))
        
        # Create default sections
        default_sections = ['CSE A', 'CSE B', 'CSM', 'ECE', 'COS']
        for section_name in default_sections:
            cursor.execute('INSERT OR IGNORE INTO sections (name) VALUES (?)', (section_name,))
        
        conn.commit()
    
    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_token(self):
        """Generate a secure random token"""
        return secrets.token_urlsafe(32)
    
    def authenticate_user(self, email, password, role):
        """Authenticate user with email, password, and role"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self._hash_password(password)
        
        cursor.execute('''
            SELECT id, email, name, role, is_active
            FROM users 
            WHERE email = ? AND password_hash = ? AND role = ? AND is_active = 1
        ''', (email, password_hash, role))
        
        user = cursor.fetchone()
        
        if user:
            user_id, user_email, name, user_role, is_active = user
            
            # Generate session token
            token = self._generate_token()
            expires_at = datetime.now() + timedelta(hours=24)  # Token expires in 24 hours
            
            cursor.execute('''
                INSERT INTO user_sessions (user_id, token, expires_at)
                VALUES (?, ?, ?)
            ''', (user_id, token, expires_at))
            
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'user': {
                    'id': user_id,
                    'email': user_email,
                    'name': name,
                    'role': user_role
                },
                'token': token
            }
        
        conn.close()
        return {
            'success': False,
            'error': 'Invalid credentials'
        }
    
    def verify_token(self, token):
        """Verify if token is valid and not expired"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.email, u.name, u.role, s.expires_at
            FROM users u
            JOIN user_sessions s ON u.id = s.user_id
            WHERE s.token = ? AND s.expires_at > CURRENT_TIMESTAMP AND u.is_active = 1
        ''', (token,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user_id, email, name, role, expires_at = result
            return {
                'valid': True,
                'user': {
                    'id': user_id,
                    'email': email,
                    'name': name,
                    'role': role
                }
            }
        
        return {'valid': False}
    
    def logout_user(self, token):
        """Logout user by invalidating token"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM user_sessions WHERE token = ?', (token,))
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def get_all_teachers(self):
        """Get all teachers"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, name, role, is_active, created_at, last_login
            FROM users 
            WHERE role = 'teacher'
            ORDER BY name
        ''')
        
        teachers = cursor.fetchall()
        conn.close()
        
        return [{
            'id': t[0],
            'email': t[1],
            'name': t[2],
            'role': t[3],
            'is_active': bool(t[4]),
            'created_at': t[5],
            'last_login': t[6]
        } for t in teachers]
    
    def add_teacher(self, email, password, name):
        """Add a new teacher"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = self._hash_password(password)
            cursor.execute('''
                INSERT INTO users (email, password_hash, name, role)
                VALUES (?, ?, ?, 'teacher')
            ''', (email, password_hash, name))
            
            teacher_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'teacher': {
                    'id': teacher_id,
                    'email': email,
                    'name': name,
                    'role': 'teacher'
                }
            }
        except sqlite3.IntegrityError:
            conn.close()
            return {
                'success': False,
                'error': 'Email already exists'
            }
    
    def get_all_sections(self):
        """Get all sections"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, created_at FROM sections ORDER BY name')
        sections = cursor.fetchall()
        conn.close()
        
        return [{
            'id': s[0],
            'name': s[1],
            'created_at': s[2]
        } for s in sections]
    
    def add_section(self, name):
        """Add a new section"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO sections (name) VALUES (?)', (name,))
            section_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'section': {
                    'id': section_id,
                    'name': name
                }
            }
        except sqlite3.IntegrityError:
            conn.close()
            return {
                'success': False,
                'error': 'Section already exists'
            }