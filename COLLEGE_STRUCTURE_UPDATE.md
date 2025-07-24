# College Structure Update - Year and Section Based Uploads

## Overview
Updated the Performance Analyzer to support your college structure with years (1-4) and sections (CSE A, CSE B, CSM, ECE, COS) instead of generic assessment details.

## Changes Made

### 1. Frontend Updates

#### UploadPage.js
- **Form Fields Changed:**
  - ✅ Year selection: 1st, 2nd, 3rd, 4th Year
  - ✅ Section selection: CSE A, CSE B, CSM, ECE, COS
  - ✅ Subject name: Text input (e.g., Mathematics, Physics)
  - ✅ Assessment type: Optional dropdown (Mid-term, Final, Quiz, etc.)

- **Removed Fields:**
  - ❌ Assessment name (replaced with year/section)
  - ❌ Assessment date (auto-generated)
  - ❌ Max marks (default to 100)

#### API Service (apiService.js)
- Updated `uploadFile` function to send:
  - `subjectName` instead of `subject_name`
  - `year` and `section` instead of `assessmentName`
  - `assessmentType` as optional field

### 2. Backend Updates

#### Database Models (performance_models.py)
- **Subject Model:**
  - Added `base_subject_name` field (e.g., "Mathematics")
  - Added `year` field (1, 2, 3, 4)
  - Added `section` field (CSEA, CSEB, CSM, ECE, COS)
  - Updated `subject_name` to be full name (e.g., "Mathematics - Year 2 CSEA")

- **Assessment Model:**
  - Added `assessment_type` field (Mid-term, Final, Quiz, etc.)
  - Added `year` and `section` fields for context
  - Auto-generates assessment names with year-section context

#### Upload API (uploads.py)
- Updated to accept `year`, `section`, `subjectName`, `assessmentType`
- Creates subjects with year-section context
- Generates meaningful assessment names
- Improved error handling and validation

### 3. Database Migration
- Created migration script: `backend/migrations/add_year_section_fields.py`
- Adds new columns to existing tables
- Updates existing data to fit new structure

### 4. Testing
- Created test script: `backend/test_upload.py`
- Tests multiple year-section combinations
- Validates the new upload workflow

## College Structure Support

### Years Supported
- 1st Year
- 2nd Year  
- 3rd Year
- 4th Year

### Sections Supported
- **CSE A** - Computer Science Engineering A
- **CSE B** - Computer Science Engineering B
- **CSM** - Computer Science and Mathematics
- **ECE** - Electronics and Communication Engineering
- **COS** - Computer Science (Other Specialization)

## Teacher Workflow

### Before (Old System)
1. Select file
2. Enter assessment name
3. Enter assessment date
4. Upload

### After (New System)
1. Select file
2. **Select Year** (1st, 2nd, 3rd, 4th)
3. **Select Section** (CSE A, CSE B, CSM, ECE, COS)
4. Enter subject name (Mathematics, Physics, etc.)
5. Optionally select assessment type
6. Upload

## Data Organization

### Subject Names
- **Format:** `{Subject} - Year {Year} {Section}`
- **Examples:**
  - "Mathematics - Year 2 CSEA"
  - "Physics - Year 1 ECE"
  - "Database Systems - Year 3 CSEB"

### Assessment Names
- **Format:** `{Assessment Type} - {Subject} (Year {Year} {Section})`
- **Examples:**
  - "Mid-term Exam - Mathematics (Year 2 CSEA)"
  - "Quiz - Physics (Year 1 ECE)"
  - "Final Exam - Database Systems (Year 3 CSEB)"

## Benefits

1. **Better Organization:** Clear separation by year and section
2. **Teacher Friendly:** Matches how teachers think about their classes
3. **Scalable:** Easy to add more years or sections
4. **Multiple Uploads:** Teachers can upload multiple files for same year-section
5. **Clear Context:** Always know which year and section data belongs to

## File Requirements

### Required Columns
- Student Name or Student ID
- Score/Marks
- Student Roll Number (format: 21A91A0501)

### Optional Columns
- Email
- Phone
- Remarks
- Grade

### File Naming Suggestion
- `{subject}_{year}_{section}_{assessment_type}.xlsx`
- Example: `mathematics_2nd_csea_midterm.xlsx`

## Next Steps

1. **Run Migration:** Execute the database migration script
2. **Test Upload:** Use the test script to verify functionality
3. **Train Teachers:** Show them the new year-section workflow
4. **Monitor:** Check that data is being organized correctly

The system now perfectly matches your college structure where teachers can upload multiple files for their specific year and section combinations! 🎓