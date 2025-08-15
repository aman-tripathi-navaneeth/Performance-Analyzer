#!/usr/bin/env python3
"""
Create 5 test datasets with same students but different subjects and marks
"""
import csv
import os
import random

# Student data - same students across all datasets
students = [
    {"id": "22A91A0501", "name": "Aarav Sharma", "email": "aarav.sharma@college.edu", "phone": "9876543210"},
    {"id": "22A91A0502", "name": "Aditi Patel", "email": "aditi.patel@college.edu", "phone": "9876543211"},
    {"id": "22A91A0503", "name": "Arjun Kumar", "email": "arjun.kumar@college.edu", "phone": "9876543212"},
    {"id": "22A91A0504", "name": "Ananya Singh", "email": "ananya.singh@college.edu", "phone": "9876543213"},
    {"id": "22A91A0505", "name": "Akash Gupta", "email": "akash.gupta@college.edu", "phone": "9876543214"},
    {"id": "22A91A0506", "name": "Bhavya Reddy", "email": "bhavya.reddy@college.edu", "phone": "9876543215"},
    {"id": "22A91A0507", "name": "Chetan Rao", "email": "chetan.rao@college.edu", "phone": "9876543216"},
    {"id": "22A91A0508", "name": "Deepika Jain", "email": "deepika.jain@college.edu", "phone": "9876543217"},
    {"id": "22A91A0509", "name": "Dhruv Agarwal", "email": "dhruv.agarwal@college.edu", "phone": "9876543218"},
    {"id": "22A91A0510", "name": "Esha Verma", "email": "esha.verma@college.edu", "phone": "9876543219"},
    {"id": "22A91A0511", "name": "Farhan Ali", "email": "farhan.ali@college.edu", "phone": "9876543220"},
    {"id": "22A91A0512", "name": "Garima Mehta", "email": "garima.mehta@college.edu", "phone": "9876543221"},
    {"id": "22A91A0513", "name": "Harsh Bansal", "email": "harsh.bansal@college.edu", "phone": "9876543222"},
    {"id": "22A91A0514", "name": "Ishita Kapoor", "email": "ishita.kapoor@college.edu", "phone": "9876543223"},
    {"id": "22A91A0515", "name": "Jatin Malhotra", "email": "jatin.malhotra@college.edu", "phone": "9876543224"},
    {"id": "22A91A0516", "name": "Kavya Nair", "email": "kavya.nair@college.edu", "phone": "9876543225"},
    {"id": "22A91A0517", "name": "Laksh Tiwari", "email": "laksh.tiwari@college.edu", "phone": "9876543226"},
    {"id": "22A91A0518", "name": "Meera Saxena", "email": "meera.saxena@college.edu", "phone": "9876543227"},
    {"id": "22A91A0519", "name": "Nikhil Joshi", "email": "nikhil.joshi@college.edu", "phone": "9876543228"},
    {"id": "22A91A0520", "name": "Priya Sinha", "email": "priya.sinha@college.edu", "phone": "9876543229"},
]

# Define datasets with different subjects and performance patterns
datasets = [
    {
        "filename": "Physics_2nd_Year_CSEA.csv",
        "subject": "Physics",
        "year": "2nd Year",
        "section": "CSE A",
        "description": "Physics test - Mixed performance with some struggling students",
        "score_pattern": "mixed"  # Mix of high, medium, and low scores
    },
    {
        "filename": "Chemistry_2nd_Year_CSEA.csv", 
        "subject": "Chemistry",
        "year": "2nd Year",
        "section": "CSE A",
        "description": "Chemistry test - Generally good performance",
        "score_pattern": "good"  # Most students perform well
    },
    {
        "filename": "Data_Structures_2nd_Year_CSEA.csv",
        "subject": "Data Structures",
        "year": "2nd Year", 
        "section": "CSE A",
        "description": "Data Structures test - Challenging subject with varied results",
        "score_pattern": "challenging"  # Lower scores overall
    },
    {
        "filename": "English_2nd_Year_CSEA.csv",
        "subject": "English",
        "year": "2nd Year",
        "section": "CSE A", 
        "description": "English test - Excellent performance across the board",
        "score_pattern": "excellent"  # High scores for most students
    },
    {
        "filename": "Database_Systems_2nd_Year_CSEA.csv",
        "subject": "Database Systems",
        "year": "2nd Year",
        "section": "CSE A",
        "description": "Database Systems test - Average performance with room for improvement",
        "score_pattern": "average"  # Average scores around 70-80
    }
]

def generate_score(pattern, student_index):
    """Generate score based on pattern and student characteristics"""
    
    # Define student performance tendencies (some students are naturally better)
    student_tendencies = {
        0: 0.9,   # Aarav - excellent student
        1: 0.95,  # Aditi - top performer
        2: 0.75,  # Arjun - good student
        3: 0.85,  # Ananya - very good
        4: 0.65,  # Akash - average
        5: 0.9,   # Bhavya - excellent
        6: 0.8,   # Chetan - good
        7: 0.88,  # Deepika - very good
        8: 0.7,   # Dhruv - average
        9: 0.82,  # Esha - good
        10: 0.78, # Farhan - good
        11: 0.92, # Garima - excellent
        12: 0.73, # Harsh - average
        13: 0.87, # Ishita - very good
        14: 0.68, # Jatin - average
        15: 0.91, # Kavya - excellent
        16: 0.76, # Laksh - good
        17: 0.84, # Meera - very good
        18: 0.72, # Nikhil - average
        19: 0.86  # Priya - very good
    }
    
    base_tendency = student_tendencies.get(student_index, 0.75)
    
    if pattern == "excellent":
        # High scores (85-98)
        score = base_tendency * random.uniform(85, 98)
    elif pattern == "good":
        # Good scores (75-92)
        score = base_tendency * random.uniform(75, 92)
    elif pattern == "average":
        # Average scores (65-85)
        score = base_tendency * random.uniform(65, 85)
    elif pattern == "challenging":
        # Lower scores (50-80)
        score = base_tendency * random.uniform(50, 80)
    elif pattern == "mixed":
        # Mixed scores (45-95)
        score = base_tendency * random.uniform(45, 95)
    else:
        # Default mixed pattern
        score = base_tendency * random.uniform(60, 90)
    
    # Add some randomness
    score += random.uniform(-5, 5)
    
    # Ensure score is within bounds
    score = max(0, min(100, score))
    
    return round(score, 1)

def create_dataset(dataset_info):
    """Create a CSV dataset"""
    filename = dataset_info["filename"]
    pattern = dataset_info["score_pattern"]
    
    print(f"Creating {filename}...")
    print(f"  Subject: {dataset_info['subject']}")
    print(f"  Pattern: {dataset_info['description']}")
    
    # Create sample_data directory if it doesn't exist
    os.makedirs("sample_data", exist_ok=True)
    
    filepath = os.path.join("sample_data", filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Student ID', 'Student Name', 'Score', 'Email', 'Phone', 'Remarks']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for i, student in enumerate(students):
            score = generate_score(pattern, i)
            
            # Generate remarks based on score
            if score >= 90:
                remarks = "Excellent performance"
            elif score >= 80:
                remarks = "Very good work"
            elif score >= 70:
                remarks = "Good effort"
            elif score >= 60:
                remarks = "Satisfactory"
            elif score >= 50:
                remarks = "Needs improvement"
            else:
                remarks = "Requires attention"
            
            writer.writerow({
                'Student ID': student['id'],
                'Student Name': student['name'],
                'Score': score,
                'Email': student['email'],
                'Phone': student['phone'],
                'Remarks': remarks
            })
    
    print(f"  ✅ Created {filepath}")
    return filepath

def main():
    print("=" * 60)
    print("🎯 CREATING 5 TEST DATASETS FOR STUDENT PERFORMANCE ANALYSIS")
    print("=" * 60)
    print("📊 Same 20 students across all subjects with different performance patterns")
    print()
    
    created_files = []
    
    for dataset in datasets:
        filepath = create_dataset(dataset)
        created_files.append(filepath)
        print()
    
    print("=" * 60)
    print("✅ ALL DATASETS CREATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("📁 Created files:")
    for file in created_files:
        print(f"   - {file}")
    
    print()
    print("🚀 HOW TO USE THESE DATASETS:")
    print("1. Start your backend server: python run.py")
    print("2. Start your frontend: npm start")
    print("3. Go to Upload page in your React app")
    print("4. Upload each CSV file with these settings:")
    print()
    
    for dataset in datasets:
        print(f"   📄 {dataset['filename']}:")
        print(f"      Subject: {dataset['subject']}")
        print(f"      Year: {dataset['year']}")
        print(f"      Section: {dataset['section']}")
        print(f"      Assessment Type: General Assessment")
        print()
    
    print("🎯 EXPECTED RESULTS:")
    print("- Each student will have performance data across 5 subjects")
    print("- You'll see varied academic insights based on performance patterns")
    print("- Some students will show as 'Excellent' in some subjects, 'Average' in others")
    print("- Perfect for testing the academic insights functionality!")
    print()
    print("🔍 TEST STUDENTS TO CHECK:")
    print("- 22A91A0501 (Aarav Sharma) - Should show as excellent overall")
    print("- 22A91A0502 (Aditi Patel) - Should show as top performer")
    print("- 22A91A0505 (Akash Gupta) - Should show as average student")
    print("- 22A91A0509 (Dhruv Agarwal) - Should show mixed performance")
    print("=" * 60)

if __name__ == "__main__":
    main()