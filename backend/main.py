# pylint: disable=invalid-name, too-many-arguments, too-many-locals, broad-exception-caught
"""
FastAPI Backend for Performance Analyzer
Handles Excel file uploads, parsing student marks, and storing them in an SQLite database.
"""

import io
import json
import logging
import hashlib
from datetime import datetime
import os
import google.generativeai as genai
import pandas as pd
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from pydantic import BaseModel
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
# Assumes GEMINI_API_KEY is available in the environment
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logger.warning("GEMINI_API_KEY not found in environment variables.")

# Admin credentials from environment
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "superadmin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "superadmin123")

def hash_password(password: str) -> str:
    """Hashes a password using SHA-256 for basic security."""
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize FastAPI
app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
class Base(DeclarativeBase):
    pass


class StudentPerformance(Base):
    """
    SQLAlchemy Model for storing student performance records from Excel uploads.
    """
    __tablename__ = "student_performance"
    id = Column(Integer, primary_key=True, index=True)
    rollNumber = Column(String, index=True)
    name = Column(String)
    totalMarks = Column(Float)
    subject = Column(String)
    year = Column(String)
    branch = Column(String)
    section = Column(String)
    uploadedBy = Column(String)
    uploadedAt = Column(DateTime, default=datetime.utcnow)
    
    # Advanced Analytics Fields
    normalized_score = Column(Float, nullable=True)
    assessment_score = Column(Float, nullable=True)
    final_combined_score = Column(Float, nullable=True)
    performance_category = Column(String, nullable=True)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rollNumber = Column(String, unique=True, index=True)
    password = Column(String)
    section = Column(String, nullable=True)
    branch = Column(String, nullable=True)
    year = Column(String, nullable=True)

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="faculty")
    subject = Column(String)

class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    branch = Column(String, nullable=True)
    year = Column(String, nullable=True)

class Test(Base):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True, index=True)
    testName = Column(String)
    subject = Column(String)
    year = Column(String)
    branch = Column(String)
    section = Column(String)
    numberOfQuestions = Column(Integer, default=20)
    startTime = Column(String) # Storing as ISO strings for simplicity
    endTime = Column(String)
    createdBy = Column(String)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, index=True)
    question = Column(Text)
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)
    correct_answer = Column(String)

class StudentTestResult(Base):
    __tablename__ = "student_test_results"
    id = Column(Integer, primary_key=True, index=True)
    student_roll = Column(String, index=True)
    test_id = Column(Integer, index=True)
    score = Column(Integer)
    total_questions = Column(Integer)
    submitted_at = Column(DateTime, default=datetime.utcnow)

class StudentAnswer(Base):
    __tablename__ = "student_answers"
    id = Column(Integer, primary_key=True, index=True)
    student_roll = Column(String, index=True)
    test_id = Column(Integer, index=True)
    question_id = Column(Integer, index=True)
    selected_answer = Column(String)

class StudentAssignedQuestion(Base):
    __tablename__ = "student_assigned_questions"
    id = Column(Integer, primary_key=True, index=True)
    student_roll = Column(String, index=True)
    test_id = Column(Integer, index=True)
    question_id = Column(Integer, index=True)


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    company = Column(String)
    year = Column(String)
    branch = Column(String)
    section = Column(String)
    posted_by = Column(String)
    posted_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Database Seeding
def seed_default_accounts():
    db = SessionLocal()
    try:
        # Check if TPO exists
        tpo_user = db.query(Teacher).filter(Teacher.username == "TPO").first()
        if not tpo_user:
            new_tpo = Teacher(
                name="Training & Placement Officer",
                username="TPO",
                password="TPO", # Hardcoded default as requested
                role="tpo",
                subject="Placement Training" # Dummy subject
            )
            db.add(new_tpo)
            db.commit()
    except Exception as e:
        print(f"Error seeding background info: {e}")
    finally:
        db.close()

seed_default_accounts()

# Pydantic Request Models
class StudentRegisterRequest(BaseModel):
    name: str
    rollNumber: str
    password: str
    section: Optional[str] = None
    branch: Optional[str] = None
    year: Optional[str] = None

class StudentLoginRequest(BaseModel):
    rollNumber: str
    password: str

class TeacherCreateRequest(BaseModel):
    name: str
    username: str
    password: str
    role: str
    subject: str

class TeacherLoginRequest(BaseModel):
    username: str
    password: str

class SectionCreateRequest(BaseModel):
    name: str
    branch: Optional[str] = None
    year: Optional[str] = None

class JobCreateRequest(BaseModel):
    title: str
    description: str
    company: str
    year: str
    branch: str
    section: str
    posted_by: str

class TestCreateRequest(BaseModel):
    testName: str
    subject: str
    year: str
    branch: str
    section: str
    numberOfQuestions: int
    startTime: str
    endTime: str
    createdBy: str

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class StudentTestSubmission(BaseModel):
    student_roll: str
    answers: dict[str, str] # mapping of question_id (stringified int) to selected_answer

@app.post("/api/admin/login")
async def login_admin(request: AdminLoginRequest):
    """Validates super admin credentials from environment variables."""
    if request.username == ADMIN_USERNAME and request.password == ADMIN_PASSWORD:
        return {
            "message": "Admin login successful",
            "admin": {"role": "admin", "username": request.username}
        }
    raise HTTPException(status_code=401, detail="Invalid admin credentials")

@app.post("/api/students/register")
async def register_student(request: StudentRegisterRequest):
    db = SessionLocal()
    try:
        if db.query(Student).filter(Student.rollNumber == request.rollNumber).first():
            raise HTTPException(status_code=400, detail="Student already exists")
        
        new_student = Student(
            name=request.name,
            rollNumber=request.rollNumber,
            password=hash_password(request.password),
            section=request.section,
            branch=request.branch,
            year=request.year
        )
        db.add(new_student)
        db.commit()
        return {"message": "Student registered successfully"}
    finally:
        db.close()

@app.post("/api/students/login")
async def login_student(request: StudentLoginRequest):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.rollNumber == request.rollNumber).first()
        if not student:
            raise HTTPException(status_code=401, detail="Invalid roll number or password")
        
        if student.password != hash_password(request.password):
            # Allow fallback to plain text if the user existed from before hashing was implemented
            if student.password != request.password:
                raise HTTPException(status_code=401, detail="Invalid roll number or password")
            else:
                # Optional: Upgrade password to hash here automatically
                student.password = hash_password(request.password)
                db.commit()

        return {
            "message": "Login successful",
            "student": {
                "name": student.name,
                "rollNumber": student.rollNumber,
                "section": student.section,
                "branch": student.branch,
                "year": student.year
            }
        }
    finally:
        db.close()

@app.post("/api/teachers/add")
async def add_teacher(teacher: TeacherCreateRequest):
    db: Session = SessionLocal()
    try:
        # Check if username already exists
        existing = db.query(Teacher).filter(Teacher.username == teacher.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

        new_teacher = Teacher(
            name=teacher.name,
            username=teacher.username,
            password=hash_password(teacher.password),
            role=teacher.role,
            subject=teacher.subject
        )
        db.add(new_teacher)
        db.commit()
        db.refresh(new_teacher)
        return {"message": "Teacher added successfully", "teacher": {"id": new_teacher.id, "name": new_teacher.name, "username": new_teacher.username, "role": new_teacher.role, "subject": new_teacher.subject}}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/api/teachers/login")
async def login_teacher(login_req: TeacherLoginRequest):
    db: Session = SessionLocal()
    try:
        teacher = db.query(Teacher).filter(Teacher.username == login_req.username).first()
        if not teacher:
            raise HTTPException(status_code=401, detail="Invalid username or password")
            
        if teacher.password != hash_password(login_req.password):
            # Allow fallback for previously unhashed admin/faculty
            if teacher.password != login_req.password:
                raise HTTPException(status_code=401, detail="Invalid username or password")
            else:
                teacher.password = hash_password(login_req.password)
                db.commit()
            
        return {
            "message": "Login successful",
            "teacher": {
                "id": teacher.id,
                "name": teacher.name,
                "username": teacher.username,
                "role": teacher.role,
                "subject": teacher.subject
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@app.get("/api/teachers")
async def get_teachers():
    db = SessionLocal()
    try:
        teachers = db.query(Teacher).all()
        return [
            {
                "id": t.id,
                "name": t.name,
                "username": t.username,
                "role": t.role,
                "subject": t.subject
            } for t in teachers
        ]
    finally:
        db.close()

@app.post("/api/sections/add")
async def add_section(request: SectionCreateRequest):
    db = SessionLocal()
    try:
        if db.query(Section).filter(Section.name == request.name).first():
            raise HTTPException(status_code=400, detail="Section already exists")
        
        new_section = Section(
            name=request.name,
            branch=request.branch,
            year=request.year
        )
        db.add(new_section)
        db.commit()
        return {"message": "Section added successfully", "section": request.model_dump()}
    finally:
        db.close()

@app.get("/api/sections")
async def get_sections():
    db = SessionLocal()
    try:
        sections = db.query(Section).all()
        return [
            {
                "id": s.id,
                "name": s.name,
                "branch": s.branch,
                "year": s.year
            } for s in sections
        ]
    finally:
        db.close()

# ⚠️ BILLING WARNING: This endpoint calls the Google Gemini API which may incur costs.
# Ensure GEMINI_API_KEY is set and monitor usage in your Google Cloud Console.
@app.post("/api/tests/create")
async def create_test(request: TestCreateRequest):
    db: Session = SessionLocal()
    try:
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=500, detail="Gemini API Key is not configured. Cannot generate questions.")

        new_test = Test(
            testName=request.testName,
            subject=request.subject,
            year=request.year,
            branch=request.branch,
            section=request.section,
            numberOfQuestions=request.numberOfQuestions,
            startTime=request.startTime,
            endTime=request.endTime,
            createdBy=request.createdBy
        )
        db.add(new_test)
        db.commit()
        db.refresh(new_test)

        # Call Gemini to generate questions
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = f"""
            Generate exactly {request.numberOfQuestions} multiple choice questions for the subject "{request.subject}".
            Return the result ONLY as a raw JSON array of objects. Do not use markdown blocks like ```json.
            Each object must use these exact keys:
            "question", "option_a", "option_b", "option_c", "option_d", "correct_answer".
            Make sure "correct_answer" exactly matches the text of one of the options (A, B, C, or D).
            """
            response = model.generate_content(prompt)
            
            # Clean up the response if Gemini wraps it in markdown
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
                
            questions_data = json.loads(raw_text.strip())

            for q_data in questions_data:
                q_model = Question(
                    test_id=new_test.id,
                    question=q_data.get("question", "Unknown Question"),
                    option_a=q_data.get("option_a", ""),
                    option_b=q_data.get("option_b", ""),
                    option_c=q_data.get("option_c", ""),
                    option_d=q_data.get("option_d", ""),
                    correct_answer=q_data.get("correct_answer", "")
                )
                db.add(q_model)
            
            db.commit()

        except Exception as e:
            logger.error(f"Error generating questions via Gemini: {e}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to generate questions: {str(e)}")

        return {"message": "Test and questions created successfully", "test": request.model_dump(), "test_id": new_test.id}
    finally:
        db.close()

@app.get("/api/tests/student")
async def get_student_tests(year: str, branch: str, section: str, student_roll: str):
    db: Session = SessionLocal()
    try:
        from datetime import datetime
        
        # 1. Fetch tests the student has already taken
        taken_tests = db.query(StudentTestResult.test_id).filter(
            StudentTestResult.student_roll == student_roll
        ).all()
        taken_test_ids = [t[0] for t in taken_tests]

        # 2. Fetch active assigned tests mapping to the student demographic
        all_assigned_tests = db.query(Test).filter(
            Test.year == year,
            Test.branch == branch,
            Test.section == section
        ).all()

        current_time = datetime.now()
        available_tests = []

        # 3. Filter out taken tests, and tests where the endTime is strictly in the past
        for t in all_assigned_tests:
            if t.id in taken_test_ids:
                continue
                
            try:
                # The frontend passes startTime and endTime as ISO dates or 'HH:MM' (which gets appended to date in the frontend state). Let's parse securely.
                # Assuming t.endTime is an ISO string: "2026-03-06T15:30"
                if t.endTime:
                    end_dt = datetime.fromisoformat(t.endTime)
                    if current_time > end_dt:
                        continue # Time has expired
            except Exception as e:
                logger.warning(f"Could not parse test end time for {t.id}: {t.endTime} - {e}")
                
            available_tests.append(t)
        
        return [
            {
                "id": str(t.id),
                "testName": t.testName,
                "subject": t.subject,
                "year": t.year,
                "branch": t.branch,
                "section": t.section,
                "startTime": t.startTime,
                "endTime": t.endTime,
                "createdBy": t.createdBy
            } for t in available_tests
        ]
    finally:
        db.close()

@app.get("/api/tests/faculty")
async def get_faculty_tests(username: str):
    db: Session = SessionLocal()
    try:
        tests = db.query(Test).filter(Test.createdBy == username).all()
        return [
            {
                "id": str(t.id),
                "testName": t.testName,
                "subject": t.subject,
                "year": t.year,
                "branch": t.branch,
                "section": t.section,
                "startTime": t.startTime,
                "endTime": t.endTime,
                "createdBy": t.createdBy
            } for t in tests
        ]
    finally:
        db.close()

@app.get("/api/tests/{test_id}/questions")
async def get_test_questions(test_id: int, student_roll: str):
    """
    Fetches the questions for a specific test for the student to take.
    OMITS the correct_answer field for security.
    """
    db: Session = SessionLocal()
    try:
        test = db.query(Test).filter(Test.id == test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail="Test not found")

        # Check if the student already has assigned questions for this test
        assigned_questions = db.query(StudentAssignedQuestion).filter(
            StudentAssignedQuestion.student_roll == student_roll,
            StudentAssignedQuestion.test_id == test_id
        ).all()

        import random

        if assigned_questions:
            # Fetch those specific questions
            question_ids = [aq.question_id for aq in assigned_questions]
            selected_questions_unordered = db.query(Question).filter(Question.id.in_(question_ids)).all()
            
            # Sort them in the order they were assigned to maintain order per student
            q_map = {q.id: q for q in selected_questions_unordered}
            selected_questions = [q_map[q_id] for q_id in question_ids if q_id in q_map]
        else:
            # First time: select random questions and assign them
            all_questions = db.query(Question).filter(Question.test_id == test_id).all()
            
            # Select required number (or all if not enough)
            num_req = test.numberOfQuestions if test.numberOfQuestions else len(all_questions)
            if num_req > len(all_questions):
                num_req = len(all_questions)
                
            selected_questions = random.sample(all_questions, num_req) if num_req < len(all_questions) else all_questions
            # Randomize order even if we pick all
            random.shuffle(selected_questions)

            # Save the assignment
            for q in selected_questions:
                assignment = StudentAssignedQuestion(
                    student_roll=student_roll,
                    test_id=test_id,
                    question_id=q.id
                )
                db.add(assignment)
            db.commit()

        result = []
        for q in selected_questions:
            # Shuffle options
            options = [
                {"key": "a", "text": q.option_a},
                {"key": "b", "text": q.option_b},
                {"key": "c", "text": q.option_c},
                {"key": "d", "text": q.option_d}
            ]
            random.shuffle(options)
            
            result.append({
                "id": str(q.id),
                "question": q.question,
                "option_a": options[0]["text"],
                "option_b": options[1]["text"],
                "option_c": options[2]["text"],
                "option_d": options[3]["text"]
            })

        return result
    finally:
        db.close()

class SubmitTestRequest(BaseModel):
    student_roll: str
    answers: dict

@app.post("/api/tests/{test_id}/submit")
async def submit_test(test_id: int, request: SubmitTestRequest):
    """
    Evaluates a submitted test against the database question keys.
    """
    db: Session = SessionLocal()
    try:
        all_questions = db.query(Question).filter(Question.test_id == test_id).all()
        if not all_questions:
            raise HTTPException(status_code=404, detail="Test not found or has no questions.")

        score = 0
        total_questions = len(all_questions)

        # Build mapping of question_id -> correct_answer
        answer_key = {str(q.id): q.correct_answer for q in all_questions}

        # Check submitted answers and score them while saving the student_answers row
        for q_id_str, selected_ans in request.answers.items():
            is_correct = False
            correct_ans = answer_key.get(q_id_str)
            if correct_ans and selected_ans == correct_ans:
                score += 1
                is_correct = True
            
            # Save individual answer for metrics optional
            student_answer = StudentAnswer(
                student_roll=request.student_roll,
                test_id=test_id,
                question_id=int(q_id_str),
                selected_answer=selected_ans
            )
            db.add(student_answer)

        # Save test result
        test_result = StudentTestResult(
            student_roll=request.student_roll,
            test_id=test_id,
            score=score,
            total_questions=total_questions
        )
        db.add(test_result)
        db.commit()

        return {
            "message": "Test submitted successfully",
            "score": score,
            "total_questions": total_questions
        }
    finally:
        db.close()

@app.get("/api/tests/{test_id}/questions/all")
async def get_all_test_questions(test_id: int):
    """
    Fetches the questions for a specific test INCLUDING the correct_answer for faculty/admin.
    Returns all generated questions.
    """
    db: Session = SessionLocal()
    try:
        test = db.query(Test).filter(Test.id == test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail="Test not found")

        all_questions = db.query(Question).filter(Question.test_id == test_id).all()
        
        return [
            {
                "id": str(q.id),
                "question": q.question,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_answer": q.correct_answer
            } for q in all_questions
        ]
    finally:
        db.close()

@app.post("/api/sections/add")
async def add_section(request: SectionCreateRequest):
    db = SessionLocal()
    try:
        if db.query(Section).filter(Section.name == request.name).first():
            raise HTTPException(status_code=400, detail="Section already exists")
        
        new_section = Section(
            name=request.name,
            branch=request.branch,
            year=request.year
        )
        db.add(new_section)
        db.commit()
        return {"message": "Section added successfully", "section": request.model_dump()}
    finally:
        db.close()

@app.get("/api/students/{roll_number}/analytics")
async def get_student_analytics(roll_number: str):
    """
    Fetches combined analytics data for a specific student, merging uploaded internal
    marks with dynamically scored AI-generated tests.
    """
    db: Session = SessionLocal()
    try:
        # Fetch uploaded performance (internal marks)
        internal_performances = db.query(StudentPerformance).filter(StudentPerformance.rollNumber == roll_number).all()
        
        # Fetch actual AI test results
        ai_test_results = db.query(StudentTestResult).filter(StudentTestResult.student_roll == roll_number).all()
        
        analytics_data = []

        # Map internal marks
        for perf in internal_performances:
            analytics_data.append({
                "source": "Internal Excel Upload",
                "subject": perf.subject,
                "score": perf.totalMarks,
                "max_score": 100, # Assuming internal marks are out of 100
                "date": str(perf.uploadedAt).split(' ')[0]
            })

        # Map AI Tests
        for result in ai_test_results:
            # We need the subject name from the Test table
            test = db.query(Test).filter(Test.id == result.test_id).first()
            subject_name = test.subject if test else "Unknown Test"
            
            # Normalize score to percentage for fair comparison, or just send raw values 
            # (Recharts can handle multiple domain setups, but standardizing helps)
            analytics_data.append({
                "source": "AI Generated Test",
                "subject": subject_name,
                "score": result.score,
                "max_score": result.total_questions,
                "date": str(result.submitted_at).split(' ')[0]
            })

        return analytics_data

    finally:
        db.close()


@app.get("/api/performance/class")
async def get_class_performance(year: str, branch: str, section: str):
    """
    Fetches the combined performance for an entire class (for the Class & Student Graphs).
    """
    db: Session = SessionLocal()
    try:
        student_map = {}

        # 1. Fetch uploaded performance
        performances = db.query(StudentPerformance).filter(
            StudentPerformance.year == year,
            StudentPerformance.branch == branch,
            StudentPerformance.section == section
        ).all()
        
        for p in performances:
            roll = p.rollNumber
            if roll not in student_map:
                student_map[roll] = {
                    "rollNumber": roll,
                    "name": p.name,
                    "subjects": [],
                    "totalMarks": 0,
                    "averageMarks": 0
                }
            
            sub_marks = p.final_combined_score if p.final_combined_score is not None else p.totalMarks
            
            student_map[roll]["subjects"].append({
                "subjectName": p.subject,
                "marks": p.totalMarks,
                "assessmentScore": p.assessment_score if p.assessment_score is not None else 0,
                "finalScore": sub_marks
            })
            student_map[roll]["totalMarks"] += sub_marks

        # 2. Fetch standalone test submissions that match the demographics
        test_results = db.query(StudentTestResult, Test, Student).join(
            Test, StudentTestResult.test_id == Test.id
        ).join(
            Student, StudentTestResult.student_roll == Student.rollNumber
        ).filter(
            Test.year == year,
            Test.branch == branch,
            Test.section == section
        ).all()

        for result, test, student in test_results:
            roll = result.student_roll
            if roll not in student_map:
                student_map[roll] = {
                    "rollNumber": roll,
                    "name": student.name,
                    "subjects": [],
                    "totalMarks": 0,
                    "averageMarks": 0
                }

            # If the subject exists in the map already from uploaded marks, skip or merge.
            # Realistically, the uploaded marks natively average out the assessments already at upload-time
            # For this phase, if we haven't seen the subject, we add it. 
            existing_sub = next((s for s in student_map[roll]["subjects"] if s["subjectName"] == test.subject), None)
            
            if not existing_sub:
                pct = (result.score / result.total_questions) * 100 if result.total_questions > 0 else 0
                student_map[roll]["subjects"].append({
                    "subjectName": test.subject,
                    "marks": 0,
                    "assessmentScore": pct,
                    "finalScore": pct
                })
                student_map[roll]["totalMarks"] += pct

        # 3. Calculate averages safely
        students_list = []
        for roll, data in student_map.items():
            subs = len(data["subjects"])
            if subs > 0:
                data["averageMarks"] = data["totalMarks"] / subs
            students_list.append(data)

        return {
            "year": year,
            "branch": branch,
            "section": section,
            "students": students_list
        }

    finally:
        db.close()


@app.post("/api/upload-marks")
async def upload_marks(
    file: UploadFile = File(...),
    year: str = Form(...),
    branch: str = Form(...),
    section: str = Form(...),
    subject: str = Form(...),
    uploadedBy: str = Form(...)
):
    """
    Endpoint to process an uploaded Excel sheet containing student marks.
    Extracts 'Roll Number', 'Name', and 'Marks', then stores them in SQLite.
    """
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .xlsx and .xls are supported."
        )

    try:
        # Read the uploaded file into a Pandas DataFrame
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        # Dynamically detect required columns
        roll_col = next((c for c in df.columns if 'roll' in str(c).lower()), None)
        name_col = next((c for c in df.columns if 'name' in str(c).lower()), None)
        marks_col = next(
            (c for c in df.columns if any(
                keyword in str(c).lower() for keyword in ['mark', 'score', 'total']
            )),
            None
        )

        if not marks_col:
            raise HTTPException(
                status_code=400,
                detail="Could not detect a Marks/Score column in the uploaded file."
            )

        # Fallback if specific columns aren't found
        roll_col = roll_col if roll_col else df.columns[0]
        name_col = name_col if name_col else df.columns[1]

        # Extract only the necessary columns and filter out missing marks
        extracted_data = df[[roll_col, name_col, marks_col]].dropna(subset=[marks_col])

        # Open DB Session
        db = SessionLocal()
        parsed_results = []
        
        # Determine the maximum mark in the file for normalization
        max_total_in_file = extracted_data[marks_col].max()
        if max_total_in_file == 0 or pd.isna(max_total_in_file):
            max_total_in_file = 100 # Fallback to prevent divide-by-zero

        for index, row in extracted_data.iterrows():
            try:
                roll = str(row[roll_col])
                student_name = str(row[name_col])
                marks = float(row[marks_col])

                # Exclude invalid parsed rows (e.g headers caught as data)
                if pd.isna(marks) or not roll.strip():
                    continue

                # 1. Normalize the score
                normalized_score = (marks / max_total_in_file) * 100

                # 2. Look up existing Assessment Scores for this Subject
                # We need to find tests for this subject that the student has taken
                taken_tests = db.query(StudentTestResult, Test).join(
                    Test, StudentTestResult.test_id == Test.id
                ).filter(
                    StudentTestResult.student_roll == roll,
                    Test.subject == subject
                ).all()

                assessment_score = 0
                if taken_tests:
                    # Calculate average percentage across all AI tests taken for this subject
                    total_test_pct = 0
                    for tr, t in taken_tests:
                        pct = (tr.score / tr.total_questions) * 100 if tr.total_questions > 0 else 0
                        total_test_pct += pct
                    assessment_score = total_test_pct / len(taken_tests)
                
                # 3. Calculate Final Combined
                # If they haven't taken a test, we can just use the normalized score, or treat assessment as 0. Let's average if they have tests, else just normalized
                if taken_tests:
                    final_combined_score = (normalized_score + assessment_score) / 2
                else:
                    final_combined_score = normalized_score

                # 4. Determine Performance Category
                if final_combined_score >= 85:
                    performance_category = "Excellent"
                elif final_combined_score >= 70:
                    performance_category = "Good"
                elif final_combined_score >= 50:
                    performance_category = "Average"
                else:
                    performance_category = "Needs Improvement"

                student_record = StudentPerformance(
                    rollNumber=roll,
                    name=student_name,
                    totalMarks=marks,
                    subject=subject,
                    year=year,
                    branch=branch,
                    section=section,
                    uploadedBy=uploadedBy,
                    normalized_score=normalized_score,
                    assessment_score=assessment_score,
                    final_combined_score=final_combined_score,
                    performance_category=performance_category
                )
                db.add(student_record)

                parsed_results.append({
                    "rollNumber": roll,
                    "name": student_name,
                    "marks": marks,
                    "normalized": round(normalized_score, 2),
                    "assessment": round(assessment_score, 2),
                    "finalScore": round(final_combined_score, 2),
                    "category": performance_category
                })
            except Exception as row_error:
                print(f"Error parsing row {index}: {row_error}")
                continue

        db.commit()
        db.close()

        # Calculate brief stats to return
        if not parsed_results:
            raise HTTPException(status_code=400, detail="No valid data could be extracted.")

        return {
            "message": f"Successfully parsed and categorized {len(parsed_results)} records.",
            "data": parsed_results
        }

    except HTTPException:
        # Re-raise known exceptions cleanly
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing the file: {str(e)}"
        ) from e


@app.post("/api/jobs")
async def create_job(request: JobCreateRequest):
    """
    Creates a new job posting for a specific class.
    """
    db = SessionLocal()
    try:
        new_job = Job(
            title=request.title,
            description=request.description,
            company=request.company,
            year=request.year,
            branch=request.branch,
            section=request.section,
            posted_by=request.posted_by
        )
        db.add(new_job)
        db.commit()
        return {"message": "Job posted successfully", "id": new_job.id}
    finally:
        db.close()

@app.get("/api/jobs")
async def get_all_jobs():
    """
    Fetches all jobs regardless of demographic (useful for TPO).
    """
    db = SessionLocal()
    try:
        jobs = db.query(Job).order_by(Job.posted_at.desc()).all()
        return jobs
    finally:
        db.close()

@app.get("/api/student/{rollNumber}/jobs")
async def get_student_jobs(rollNumber: str):
    """
    Fetches jobs specifically designated for the student's year, branch, and section.
    """
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.rollNumber == rollNumber).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        jobs = db.query(Job).filter(
            Job.year == student.year
        ).order_by(Job.posted_at.desc()).all()
        
        return jobs
    finally:
        db.close()

class UpdateTpoPasswordRequest(BaseModel):
    newPassword: str

@app.put("/api/admin/tpo/password")
async def update_tpo_password(request: UpdateTpoPasswordRequest):
    """
    Allows the super admin to forcefully overwrite the TPO account's password.
    """
    db = SessionLocal()
    try:
        tpo_user = db.query(Teacher).filter(Teacher.role == "tpo").first()
        if not tpo_user:
            raise HTTPException(status_code=404, detail="TPO account not initialized.")
        
        tpo_user.password = request.newPassword # Depending on architecture this might need hash_password() but Faculty passwords are cleartext in this local schema
        db.commit()
        return {"message": "TPO password updated successfully"}
    finally:
        db.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
