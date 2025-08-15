#!/usr/bin/env python3
"""
Generate 6 datasets for 4th Year CSE A section with 60 students each
Same students in all files but different scores for different subjects
"""
import csv
import random
import os

# 60 students for 4th Year CSE A
students = [
    {"id": "22A91A4001", "name": "Aadhya Sharma", "email": "aadhya.sharma@college.edu", "phone": "9876543001"},
    {"id": "22A91A4002", "name": "Aarav Patel", "email": "aarav.patel@college.edu", "phone": "9876543002"},
    {"id": "22A91A4003", "name": "Abhinav Kumar", "email": "abhinav.kumar@college.edu", "phone": "9876543003"},
    {"id": "22A91A4004", "name": "Aditi Singh", "email": "aditi.singh@college.edu", "phone": "9876543004"},
    {"id": "22A91A4005", "name": "Aditya Gupta", "email": "aditya.gupta@college.edu", "phone": "9876543005"},
    {"id": "22A91A4006", "name": "Akash Verma", "email": "akash.verma@college.edu", "phone": "9876543006"},
    {"id": "22A91A4007", "name": "Ananya Reddy", "email": "ananya.reddy@college.edu", "phone": "9876543007"},
    {"id": "22A91A4008", "name": "Ankit Jain", "email": "ankit.jain@college.edu", "phone": "9876543008"},
    {"id": "22A91A4009", "name": "Arjun Mehta", "email": "arjun.mehta@college.edu", "phone": "9876543009"},
    {"id": "22A91A4010", "name": "Arya Nair", "email": "arya.nair@college.edu", "phone": "9876543010"},
    {"id": "22A91A4011", "name": "Bhavya Agarwal", "email": "bhavya.agarwal@college.edu", "phone": "9876543011"},
    {"id": "22A91A4012", "name": "Chetan Rao", "email": "chetan.rao@college.edu", "phone": "9876543012"},
    {"id": "22A91A4013", "name": "Deepika Bansal", "email": "deepika.bansal@college.edu", "phone": "9876543013"},
    {"id": "22A91A4014", "name": "Dhruv Malhotra", "email": "dhruv.malhotra@college.edu", "phone": "9876543014"},
    {"id": "22A91A4015", "name": "Esha Kapoor", "email": "esha.kapoor@college.edu", "phone": "9876543015"},
    {"id": "22A91A4016", "name": "Farhan Ali", "email": "farhan.ali@college.edu", "phone": "9876543016"},
    {"id": "22A91A4017", "name": "Garima Saxena", "email": "garima.saxena@college.edu", "phone": "9876543017"},
    {"id": "22A91A4018", "name": "Harsh Tiwari", "email": "harsh.tiwari@college.edu", "phone": "9876543018"},
    {"id": "22A91A4019", "name": "Ishita Joshi", "email": "ishita.joshi@college.edu", "phone": "9876543019"},
    {"id": "22A91A4020", "name": "Jatin Sinha", "email": "jatin.sinha@college.edu", "phone": "9876543020"},
    {"id": "22A91A4021", "name": "Kavya Mishra", "email": "kavya.mishra@college.edu", "phone": "9876543021"},
    {"id": "22A91A4022", "name": "Laksh Pandey", "email": "laksh.pandey@college.edu", "phone": "9876543022"},
    {"id": "22A91A4023", "name": "Meera Chopra", "email": "meera.chopra@college.edu", "phone": "9876543023"},
    {"id": "22A91A4024", "name": "Nikhil Bhatt", "email": "nikhil.bhatt@college.edu", "phone": "9876543024"},
    {"id": "22A91A4025", "name": "Priya Arora", "email": "priya.arora@college.edu", "phone": "9876543025"},
    {"id": "22A91A4026", "name": "Rahul Khanna", "email": "rahul.khanna@college.edu", "phone": "9876543026"},
    {"id": "22A91A4027", "name": "Riya Goyal", "email": "riya.goyal@college.edu", "phone": "9876543027"},
    {"id": "22A91A4028", "name": "Rohan Mittal", "email": "rohan.mittal@college.edu", "phone": "9876543028"},
    {"id": "22A91A4029", "name": "Sakshi Bhatia", "email": "sakshi.bhatia@college.edu", "phone": "9876543029"},
    {"id": "22A91A4030", "name": "Shivam Agrawal", "email": "shivam.agrawal@college.edu", "phone": "9876543030"},
    {"id": "22A91A4031", "name": "Shreya Dubey", "email": "shreya.dubey@college.edu", "phone": "9876543031"},
    {"id": "22A91A4032", "name": "Tanvi Sharma", "email": "tanvi.sharma@college.edu", "phone": "9876543032"},
    {"id": "22A91A4033", "name": "Uday Kiran", "email": "uday.kiran@college.edu", "phone": "9876543033"},
    {"id": "22A91A4034", "name": "Varun Sethi", "email": "varun.sethi@college.edu", "phone": "9876543034"},
    {"id": "22A91A4035", "name": "Vidya Iyer", "email": "vidya.iyer@college.edu", "phone": "9876543035"},
    {"id": "22A91A4036", "name": "Yash Thakur", "email": "yash.thakur@college.edu", "phone": "9876543036"},
    {"id": "22A91A4037", "name": "Zara Khan", "email": "zara.khan@college.edu", "phone": "9876543037"},
    {"id": "22A91A4038", "name": "Abhishek Roy", "email": "abhishek.roy@college.edu", "phone": "9876543038"},
    {"id": "22A91A4039", "name": "Anjali Das", "email": "anjali.das@college.edu", "phone": "9876543039"},
    {"id": "22A91A4040", "name": "Aryan Ghosh", "email": "aryan.ghosh@college.edu", "phone": "9876543040"},
    {"id": "22A91A4041", "name": "Divya Pillai", "email": "divya.pillai@college.edu", "phone": "9876543041"},
    {"id": "22A91A4042", "name": "Gaurav Soni", "email": "gaurav.soni@college.edu", "phone": "9876543042"},
    {"id": "22A91A4043", "name": "Harini Menon", "email": "harini.menon@college.edu", "phone": "9876543043"},
    {"id": "22A91A4044", "name": "Karan Bajaj", "email": "karan.bajaj@college.edu", "phone": "9876543044"},
    {"id": "22A91A4045", "name": "Lavanya Rao", "email": "lavanya.rao@college.edu", "phone": "9876543045"},
    {"id": "22A91A4046", "name": "Manish Goel", "email": "manish.goel@college.edu", "phone": "9876543046"},
    {"id": "22A91A4047", "name": "Nandini Shah", "email": "nandini.shah@college.edu", "phone": "9876543047"},
    {"id": "22A91A4048", "name": "Omkar Patil", "email": "omkar.patil@college.edu", "phone": "9876543048"},
    {"id": "22A91A4049", "name": "Pooja Kulkarni", "email": "pooja.kulkarni@college.edu", "phone": "9876543049"},
    {"id": "22A91A4050", "name": "Rajesh Yadav", "email": "rajesh.yadav@college.edu", "phone": "9876543050"},
    {"id": "22A91A4051", "name": "Sneha Desai", "email": "sneha.desai@college.edu", "phone": "9876543051"},
    {"id": "22A91A4052", "name": "Tarun Jha", "email": "tarun.jha@college.edu", "phone": "9876543052"},
    {"id": "22A91A4053", "name": "Urmila Pandya", "email": "urmila.pandya@college.edu", "phone": "9876543053"},
    {"id": "22A91A4054", "name": "Vikram Singh", "email": "vikram.singh@college.edu", "phone": "9876543054"},
    {"id": "22A91A4055", "name": "Yamini Reddy", "email": "yamini.reddy@college.edu", "phone": "9876543055"},
    {"id": "22A91A4056", "name": "Aman Verma", "email": "aman.verma@college.edu", "phone": "9876543056"},
    {"id": "22A91A4057", "name": "Bindu Nair", "email": "bindu.nair@college.edu", "phone": "9876543057"},
    {"id": "22A91A4058", "name": "Chirag Patel", "email": "chirag.patel@college.edu", "phone": "9876543058"},
    {"id": "22A91A4059", "name": "Disha Gupta", "email": "disha.gupta@college.edu", "phone": "9876543059"},
    {"id": "22A91A4060", "name": "Ekta Sharma", "email": "ekta.sharma@college.edu", "phone": "9876543060"}
]

# 6 different subjects for 4th year CSE
subjects = [
    {"name": "Machine Learning", "code": "CS401", "max_marks": 100},
    {"name": "Software Engineering", "code": "CS402", "max_marks": 100},
    {"name": "Computer Networks", "code": "CS403", "max_marks": 100},
    {"name": "Database Management Systems", "code": "CS404", "max_marks": 100},
    {"name": "Artificial Intelligence", "code": "CS405", "max_marks": 100},
    {"name": "Compiler Design", "code": "CS406", "max_marks": 100}
]

def generate_realistic_scores(num_students):
    """Generate realistic score distribution"""
    scores = []
    
    # Create a realistic distribution
    # 10% excellent (90-100)
    # 25% very good (80-89)
    # 35% good (70-79)
    # 20% average (60-69)
    # 10% below average (50-59)
    
    excellent_count = int(num_students * 0.10)
    very_good_count = int(num_students * 0.25)
    good_count = int(num_students * 0.35)
    average_count = int(num_students * 0.20)
    below_average_count = num_students - (excellent_count + very_good_count + good_count + average_count)
    
    # Generate scores for each category
    scores.extend([random.randint(90, 100) for _ in range(excellent_count)])
    scores.extend([random.randint(80, 89) for _ in range(very_good_count)])
    scores.extend([random.randint(70, 79) for _ in range(good_count)])
    scores.extend([random.randint(60, 69) for _ in range(average_count)])
    scores.extend([random.randint(50, 59) for _ in range(below_average_count)])
    
    # Shuffle to randomize order
    random.shuffle(scores)
    return scores

def create_dataset(subject_info, filename):
    """Create a CSV dataset for a specific subject"""
    scores = generate_realistic_scores(len(students))
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['student_id', 'student_name', 'score', 'email', 'phone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write student data with scores
        for i, student in enumerate(students):
            writer.writerow({
                'student_id': student['id'],
                'student_name': student['name'],
                'score': scores[i],
                'email': student['email'],
                'phone': student['phone']
            })
    
    print(f"✅ Created {filename} with {len(students)} students for {subject_info['name']}")

def main():
    print("🚀 Generating 6 datasets for 4th Year CSE A section...")
    print(f"📊 Each dataset will contain {len(students)} students")
    print("=" * 60)
    
    # Create sample_data directory if it doesn't exist
    os.makedirs('sample_data', exist_ok=True)
    
    # Generate datasets for each subject
    for i, subject in enumerate(subjects, 1):
        filename = f"sample_data/{subject['code'].lower()}_{subject['name'].lower().replace(' ', '_')}_4th_year_cse_a.csv"
        create_dataset(subject, filename)
    
    print("=" * 60)
    print("🎉 All datasets generated successfully!")
    print("\n📁 Generated files:")
    for subject in subjects:
        filename = f"sample_data/{subject['code'].lower()}_{subject['name'].lower().replace(' ', '_')}_4th_year_cse_a.csv"
        print(f"   - {filename}")
    
    print(f"\n📈 Dataset Statistics:")
    print(f"   - Students per file: {len(students)}")
    print(f"   - Total files: {len(subjects)}")
    print(f"   - Year: 4th Year")
    print(f"   - Section: CSE A")
    print(f"   - Score distribution: Realistic (10% excellent, 25% very good, 35% good, 20% average, 10% below average)")

if __name__ == "__main__":
    main()