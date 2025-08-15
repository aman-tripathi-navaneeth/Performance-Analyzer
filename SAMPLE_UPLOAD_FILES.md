# 📊 Sample Upload Files for Performance Analyzer v2

## 🎯 Quick Test Files

### 1. Simple Format (Single Assessment)
**File**: `Sample_Mathematics_2nd_Year.xlsx`

| Student ID | Student Name | Score | Email | Phone | Remarks |
|------------|--------------|-------|-------|-------|---------|
| 22A91A0501 | Aarav Sharma | 85.5 | aarav.sharma@college.edu | 9876543210 | Excellent |
| 22A91A0502 | Aditi Patel | 78.3 | aditi.patel@college.edu | 9876543211 | Good |
| 22A91A0503 | Arjun Kumar | 92.1 | arjun.kumar@college.edu | 9876543212 | Outstanding |
| 22A91A0504 | Ananya Singh | 65.7 | ananya.singh@college.edu | 9876543213 | Needs improvement |
| 22A91A0505 | Akash Gupta | 88.9 | akash.gupta@college.edu | 9876543214 | Very good |

### 2. Multiple Assessments Format
**File**: `Sample_Data_Structures_Complete.xlsx`

| Student ID | Student Name | Mid-term | Unit Test 1 | Unit Test 2 | Final Exam | Email | Phone |
|------------|--------------|----------|-------------|-------------|------------|-------|-------|
| 22A91A0501 | Aarav Sharma | 85 | 88 | 92 | 89 | aarav.sharma@college.edu | 9876543210 |
| 22A91A0502 | Aditi Patel | 78 | 82 | 85 | 80 | aditi.patel@college.edu | 9876543211 |
| 22A91A0503 | Arjun Kumar | 92 | 90 | 94 | 91 | arjun.kumar@college.edu | 9876543212 |
| 22A91A0504 | Ananya Singh | 65 | 68 | 72 | 70 | ananya.singh@college.edu | 9876543213 |
| 22A91A0505 | Akash Gupta | 88 | 85 | 90 | 87 | akash.gupta@college.edu | 9876543214 |

### 3. CRT (Weekly Tests) Format
**File**: `Sample_CRT_Weekly_Tests.xlsx`

| Student ID | Student Name | Week | CRT Score | Email | Phone |
|------------|--------------|------|-----------|-------|-------|
| 22A91A0501 | Aarav Sharma | 1 | 85 | aarav.sharma@college.edu | 9876543210 |
| 22A91A0501 | Aarav Sharma | 2 | 88 | aarav.sharma@college.edu | 9876543210 |
| 22A91A0501 | Aarav Sharma | 3 | 92 | aarav.sharma@college.edu | 9876543210 |
| 22A91A0502 | Aditi Patel | 1 | 78 | aditi.patel@college.edu | 9876543211 |
| 22A91A0502 | Aditi Patel | 2 | 82 | aditi.patel@college.edu | 9876543211 |
| 22A91A0502 | Aditi Patel | 3 | 85 | aditi.patel@college.edu | 9876543211 |

## 📋 Upload Instructions

### Step 1: Prepare Your File
1. **Use Excel (.xlsx) format** - CSV files are also supported
2. **Include required columns**:
   - `Student ID` (or `student_id`)
   - `Student Name` (or `student_name`)
   - `Score` (or assessment column names)
3. **Optional columns**:
   - `Email`
   - `Phone`
   - `Remarks`

### Step 2: Upload Process
1. **Login** to the application (aman@gmail.com / aman123)
2. **Navigate** to Upload page
3. **Select subject name** (e.g., "Mathematics", "Data Structures")
4. **Choose subject type**:
   - `regular` - for mid-terms, unit tests, final exams
   - `crt` - for weekly coding round tests
   - `programming` - for competitive programming scores
5. **Upload your Excel file**
6. **Click Upload** and wait for processing

### Step 3: Verify Upload
1. **Check Students page** - new students should appear
2. **View Class Performance** - analytics should update
3. **Check individual student profiles** - performance data should be visible

## 🎯 Test Scenarios

### Scenario 1: Basic Upload
- **File**: Simple format with 5-10 students
- **Subject**: "Test Mathematics"
- **Type**: Regular
- **Expected**: Students appear in Students page

### Scenario 2: Multiple Assessments
- **File**: Multiple columns (Mid-term, Unit Test 1, Unit Test 2)
- **Subject**: "Advanced Data Structures"
- **Type**: Regular
- **Expected**: All assessments visible in student profiles

### Scenario 3: CRT Data
- **File**: Weekly test format with repeated student IDs
- **Subject**: "Programming Fundamentals"
- **Type**: CRT
- **Expected**: Weekly trends visible in analytics

## 📊 Sample Data Creation

### Using Excel:
1. **Open Excel**
2. **Create headers** as shown in examples above
3. **Add student data** (5-20 students recommended)
4. **Save as .xlsx** format
5. **Upload** to the system

### Using Google Sheets:
1. **Create spreadsheet** with same format
2. **Download as .xlsx**
3. **Upload** to the system

## 🔧 Troubleshooting

### Common Issues:
1. **"Invalid file format"** - Ensure file is .xlsx or .csv
2. **"Missing required columns"** - Check column names match exactly
3. **"No data found"** - Verify file has data beyond headers
4. **"Upload failed"** - Check file size (max 16MB)

### File Requirements:
- **Maximum size**: 16MB
- **Supported formats**: .xlsx, .xls, .csv
- **Required columns**: Student ID, Student Name, Score
- **Data types**: Text for names, numbers for scores

## 📈 Expected Results

After successful upload:
- ✅ **Students page** shows new students
- ✅ **Dashboard** displays updated statistics
- ✅ **Class Performance** shows analytics
- ✅ **Student Profiles** contain performance data
- ✅ **Upload History** shows successful upload

## 🎉 Success Indicators

- **Upload confirmation** message appears
- **Students count** increases in dashboard
- **Performance charts** show new data
- **No error messages** in console

---

**💡 Tip**: Start with the simple format to test basic functionality, then try more complex formats for advanced features! 