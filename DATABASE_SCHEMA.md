# 🗄️ Student Performance Analyzer - Complete Database Schema

## 📊 **Database Overview**
The Student Performance Analyzer uses **SQLite** as the primary database with two main components:
- **SQLAlchemy ORM Models** for performance data (students, subjects, assessments, performance records)
- **Raw SQLite Tables** for user management (users, sessions, sections)

---

## 🎓 **Performance Data Tables (SQLAlchemy)**

### **1. Students Table**
Stores student information and profiles.

```sql
CREATE TABLE students (
    id VARCHAR(36) PRIMARY KEY,                    -- UUID format
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    student_roll_number VARCHAR(50) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `PRIMARY KEY (id)`
- `UNIQUE INDEX (student_roll_number)`

**Sample Data:**
```sql
INSERT INTO students VALUES 
('f8ea6a5b-2739-48ff-aa51-ea3703565220', 'Aarav', 'Sharma', '22A91A0501', '2025-07-29 01:52:17'),
('d1308af4-599f-45e8-8005-6d9c3a19fc7c', 'Aditi', 'Patel', '22A91A0502', '2025-07-29 01:52:17');
```

---

### **2. Subjects Table**
Stores subject information with year and section context.

```sql
CREATE TABLE subjects (
    id VARCHAR(36) PRIMARY KEY,                    -- UUID format
    subject_name VARCHAR(200) NOT NULL,           -- Full name: "Mathematics - Year 2 CSE A"
    base_subject_name VARCHAR(100),               -- Base name: "Mathematics"
    year INTEGER,                                 -- 1, 2, 3, 4
    section VARCHAR(10),                          -- CSE A, CSE B, CSM, ECE, COS
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_subject_year_section UNIQUE (base_subject_name, year, section)
);
```

**Indexes:**
- `PRIMARY KEY (id)`
- `UNIQUE INDEX (base_subject_name, year, section)`

**Sample Data:**
```sql
INSERT INTO subjects VALUES 
('c57a6458-6086-4d0e-aca0-e3f53fe08b57', 'Mathematics Test - Year 2 CSE A', 'Mathematics Test', 2, 'CSE A', '2025-07-29 01:52:17'),
('b8f9c123-4567-89ab-cdef-123456789abc', 'Physics - Year 2 CSE A', 'Physics', 2, 'CSE A', '2025-07-29 02:15:30');
```

---

### **3. Assessments Table**
Stores assessment/exam information linked to subjects.

```sql
CREATE TABLE assessments (
    id VARCHAR(36) PRIMARY KEY,                    -- UUID format
    assessment_name VARCHAR(200) NOT NULL,        -- "General Assessment - Mathematics Test (Year 2 CSE A)"
    assessment_date DATE NOT NULL,
    assessment_type VARCHAR(50),                  -- "General Assessment", "Mid-term", "Final", "Quiz"
    max_marks FLOAT NOT NULL,                     -- Maximum possible marks
    year INTEGER,                                 -- 1, 2, 3, 4
    section VARCHAR(10),                          -- CSE A, CSE B, CSM, ECE, COS
    subject_id VARCHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);
```

**Indexes:**
- `PRIMARY KEY (id)`
- `FOREIGN KEY INDEX (subject_id)`

**Sample Data:**
```sql
INSERT INTO assessments VALUES 
('f4879a4f-2018-4fca-a99e-57d1651478e5', 'General Assessment - Mathematics Test (Year 2 CSE A)', '2025-07-29', 'General Assessment', 100.0, 2, 'CSE A', 'c57a6458-6086-4d0e-aca0-e3f53fe08b57', '2025-07-29 01:52:17');
```

---

### **4. Performance Records Table**
Stores individual student performance data for each assessment.

```sql
CREATE TABLE performance_records (
    id VARCHAR(36) PRIMARY KEY,                    -- UUID format
    marks_obtained FLOAT NOT NULL,                -- Actual marks scored
    raw_data_from_excel TEXT,                     -- JSON string of original Excel row data
    student_id VARCHAR(36) NOT NULL,
    assessment_id VARCHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (assessment_id) REFERENCES assessments(id)
);
```

**Indexes:**
- `PRIMARY KEY (id)`
- `FOREIGN KEY INDEX (student_id)`
- `FOREIGN KEY INDEX (assessment_id)`

**Sample Data:**
```sql
INSERT INTO performance_records VALUES 
('abc123-def4-5678-90ab-cdef12345678', 85.0, '{"student_id": "22A91A0501", "student_name": "Aarav Sharma", "score": 85, "email": "aarav.sharma@college.edu", "phone": 9876543210}', 'f8ea6a5b-2739-48ff-aa51-ea3703565220', 'f4879a4f-2018-4fca-a99e-57d1651478e5', '2025-07-29 01:52:17');
```

---

## 👥 **User Management Tables (Raw SQLite)**

### **5. Users Table**
Stores admin and teacher account information.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL,                  -- SHA-256 hashed password
    name TEXT NOT NULL,                           -- Full name
    role TEXT NOT NULL DEFAULT 'teacher',        -- 'admin' or 'teacher'
    is_active BOOLEAN DEFAULT 1,                 -- Account status
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    
    UNIQUE(email, role)                           -- Same email can have different roles
);
```

**Indexes:**
- `PRIMARY KEY (id)`
- `UNIQUE INDEX (email, role)`

**Sample Data:**
```sql
INSERT INTO users VALUES 
(1, 'aman@gmail.com', 'hashed_password_admin', 'Administrator', 'admin', 1, '2025-07-28 12:37:09', '2025-07-29 10:15:30'),
(2, 'aman@gmail.com', 'hashed_password_teacher', 'Teacher', 'teacher', 1, '2025-07-28 12:37:09', '2025-07-29 09:45:20'),
(3, 'john.doe@college.edu', 'hashed_password_john', 'John Doe', 'teacher', 1, '2025-07-29 14:22:15', NULL);
```

---

### **6. User Sessions Table**
Manages authentication tokens for logged-in users.

```sql
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,                   -- Authentication token
    expires_at TIMESTAMP NOT NULL,               -- Token expiration (24 hours)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Indexes:**
- `PRIMARY KEY (id)`
- `UNIQUE INDEX (token)`
- `FOREIGN KEY INDEX (user_id)`

**Sample Data:**
```sql
INSERT INTO user_sessions VALUES 
(1, 1, '316k4mHo3oDtdS0CoErfXYZ123ABC', '2025-07-30 10:15:30', '2025-07-29 10:15:30'),
(2, 3, 'abc123XYZ789def456GHI012JKL', '2025-07-30 14:22:15', '2025-07-29 14:22:15');
```

---

### **7. Sections Table**
Stores class section information.

```sql
CREATE TABLE sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,                    -- Section name: "CSE A", "ECE B", etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `PRIMARY KEY (id)`
- `UNIQUE INDEX (name)`

**Sample Data:**
```sql
INSERT INTO sections VALUES 
(1, 'CSE A', '2025-07-28 12:37:09'),
(2, 'CSE B', '2025-07-28 12:37:09'),
(3, 'CSM', '2025-07-28 12:37:09'),
(4, 'ECE', '2025-07-28 12:37:09'),
(5, 'COS', '2025-07-28 12:37:09'),
(6, 'CSE C', '2025-07-29 15:30:45');
```

---

### **8. Teacher Sections Table**
Links teachers to sections (for future assignment functionality).

```sql
CREATE TABLE teacher_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,                     -- Teacher user ID
    section_id INTEGER NOT NULL,                  -- Section ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (section_id) REFERENCES sections(id),
    UNIQUE(user_id, section_id)                   -- Prevent duplicate assignments
);
```

**Indexes:**
- `PRIMARY KEY (id)`
- `FOREIGN KEY INDEX (user_id)`
- `FOREIGN KEY INDEX (section_id)`
- `UNIQUE INDEX (user_id, section_id)`

---

## 🔗 **Relationships & Foreign Keys**

### **Performance Data Relationships**
```
students (1) ←→ (N) performance_records
subjects (1) ←→ (N) assessments
assessments (1) ←→ (N) performance_records

students ←→ performance_records ←→ assessments ←→ subjects
```

### **User Management Relationships**
```
users (1) ←→ (N) user_sessions
users (1) ←→ (N) teacher_sections ←→ (1) sections
```

---

## 📈 **Database Statistics (Current)**

### **Performance Data**
- **Students**: 23 records
- **Subjects**: 16 records  
- **Assessments**: 15 records
- **Performance Records**: 103 records

### **User Management**
- **Users**: 3 records (1 admin, 2 teachers)
- **Sections**: 6 records
- **Active Sessions**: Variable (based on logins)

---

## 🔍 **Key Queries & Indexes**

### **Most Common Queries**

#### **1. Get Student Performance Summary**
```sql
SELECT 
    s.student_roll_number,
    s.first_name,
    s.last_name,
    AVG(pr.marks_obtained * 100.0 / a.max_marks) as avg_percentage,
    COUNT(pr.id) as total_assessments
FROM students s
JOIN performance_records pr ON s.id = pr.student_id
JOIN assessments a ON pr.assessment_id = a.id
WHERE s.student_roll_number = '22A91A0501'
GROUP BY s.id;
```

#### **2. Get Subject-wise Performance**
```sql
SELECT 
    sub.subject_name,
    AVG(pr.marks_obtained * 100.0 / a.max_marks) as avg_percentage,
    COUNT(pr.id) as assessment_count
FROM subjects sub
JOIN assessments a ON sub.id = a.subject_id
JOIN performance_records pr ON a.id = pr.assessment_id
JOIN students s ON pr.student_id = s.id
WHERE s.student_roll_number = '22A91A0501'
GROUP BY sub.id;
```

#### **3. Get Class Performance Overview**
```sql
SELECT 
    sub.base_subject_name,
    sub.year,
    sub.section,
    AVG(pr.marks_obtained * 100.0 / a.max_marks) as class_average,
    COUNT(DISTINCT s.id) as student_count
FROM subjects sub
JOIN assessments a ON sub.id = a.subject_id
JOIN performance_records pr ON a.id = pr.assessment_id
JOIN students s ON pr.student_id = s.id
GROUP BY sub.base_subject_name, sub.year, sub.section;
```

---

## 🛡️ **Security & Constraints**

### **Data Integrity**
- **Primary Keys**: All tables have proper primary keys
- **Foreign Keys**: Referential integrity maintained
- **Unique Constraints**: Prevent duplicate students, subjects, sections
- **NOT NULL**: Critical fields cannot be empty

### **Authentication Security**
- **Password Hashing**: SHA-256 hashed passwords
- **Token Expiration**: 24-hour session timeout
- **Role-based Access**: Admin vs Teacher permissions
- **Unique Tokens**: Prevent session hijacking

### **Data Validation**
- **Email Format**: Validated at application level
- **Password Strength**: Minimum 6 characters
- **Student Roll Numbers**: Unique across system
- **Marks Range**: 0 to max_marks validation

---

## 📊 **Performance Considerations**

### **Indexes for Performance**
```sql
-- Performance Records (most queried)
CREATE INDEX idx_performance_student ON performance_records(student_id);
CREATE INDEX idx_performance_assessment ON performance_records(assessment_id);
CREATE INDEX idx_performance_created ON performance_records(created_at);

-- Students (frequently searched)
CREATE INDEX idx_student_roll ON students(student_roll_number);
CREATE INDEX idx_student_name ON students(first_name, last_name);

-- Assessments (filtered by date/type)
CREATE INDEX idx_assessment_date ON assessments(assessment_date);
CREATE INDEX idx_assessment_subject ON assessments(subject_id);

-- User Sessions (token lookups)
CREATE INDEX idx_session_token ON user_sessions(token);
CREATE INDEX idx_session_expires ON user_sessions(expires_at);
```

### **Query Optimization**
- **Composite Indexes**: For multi-column WHERE clauses
- **Covering Indexes**: Include SELECT columns in index
- **Partial Indexes**: For active users/sessions only

---

## 🔄 **Database Migrations**

### **Version History**
1. **v1.0**: Initial performance tables (students, subjects, assessments, performance_records)
2. **v1.1**: Added year/section fields to subjects and assessments
3. **v1.2**: Added user management tables (users, sessions, sections, teacher_sections)
4. **v1.3**: Enhanced constraints and indexes

### **Migration Scripts**
Located in: `backend/migrations/`
- `add_year_section_fields.py` - Adds year/section support

---

## 📁 **Database Files**

### **SQLite Database**
- **Location**: `backend/performance_analyzer.db`
- **Size**: ~2MB (with sample data)
- **Backup**: Recommended daily backups

### **Configuration**
```python
# backend/app/config.py
DATABASE_PATH = 'performance_analyzer.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///performance_analyzer.db'
```

---

## 🎯 **Summary**

The Student Performance Analyzer database consists of **8 main tables**:

### **Core Performance Tables** (SQLAlchemy ORM)
1. **students** - Student profiles and information
2. **subjects** - Subject definitions with year/section context  
3. **assessments** - Exam/test definitions linked to subjects
4. **performance_records** - Individual student scores and performance data

### **User Management Tables** (Raw SQLite)
5. **users** - Admin and teacher accounts
6. **user_sessions** - Authentication token management
7. **sections** - Class section definitions
8. **teacher_sections** - Teacher-section assignments (future use)

### **Key Features**
- ✅ **UUID Primary Keys** for performance data
- ✅ **Referential Integrity** with foreign keys
- ✅ **Unique Constraints** prevent duplicates
- ✅ **Role-based Security** with hashed passwords
- ✅ **Flexible Subject System** with year/section support
- ✅ **JSON Storage** for raw Excel data preservation
- ✅ **Comprehensive Indexing** for query performance

The schema supports the complete student performance analysis workflow from data upload to detailed academic insights generation! 🚀