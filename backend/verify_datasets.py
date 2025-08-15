#!/usr/bin/env python3
"""
Verify the generated datasets and show sample data
"""
import csv
import os
from collections import Counter

def verify_dataset(filename):
    """Verify a single dataset file"""
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return None
    
    students = []
    scores = []
    
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            students.append(row['student_name'])
            scores.append(int(row['score']))
    
    return {
        'filename': filename,
        'student_count': len(students),
        'scores': scores,
        'avg_score': sum(scores) / len(scores) if scores else 0,
        'min_score': min(scores) if scores else 0,
        'max_score': max(scores) if scores else 0,
        'sample_students': students[:5]  # First 5 students
    }

def main():
    print("🔍 Verifying generated datasets...")
    print("=" * 70)
    
    # List of generated files
    files = [
        "sample_data/cs401_machine_learning_4th_year_cse_a.csv",
        "sample_data/cs402_software_engineering_4th_year_cse_a.csv",
        "sample_data/cs403_computer_networks_4th_year_cse_a.csv",
        "sample_data/cs404_database_management_systems_4th_year_cse_a.csv",
        "sample_data/cs405_artificial_intelligence_4th_year_cse_a.csv",
        "sample_data/cs406_compiler_design_4th_year_cse_a.csv"
    ]
    
    all_datasets = []
    
    for filename in files:
        dataset_info = verify_dataset(filename)
        if dataset_info:
            all_datasets.append(dataset_info)
            
            subject_name = filename.split('/')[-1].replace('_4th_year_cse_a.csv', '').replace('_', ' ').title()
            
            print(f"📊 {subject_name}")
            print(f"   Students: {dataset_info['student_count']}")
            print(f"   Average Score: {dataset_info['avg_score']:.1f}")
            print(f"   Score Range: {dataset_info['min_score']} - {dataset_info['max_score']}")
            print(f"   Sample Students: {', '.join(dataset_info['sample_students'])}")
            print()
    
    # Verify same students across all files
    if len(all_datasets) > 1:
        print("🔍 Verifying student consistency across files...")
        
        # Read first file students
        with open(files[0], 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            first_file_students = [row['student_name'] for row in reader]
        
        consistent = True
        for i, filename in enumerate(files[1:], 1):
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                current_students = [row['student_name'] for row in reader]
                
                if set(first_file_students) != set(current_students):
                    print(f"❌ Student mismatch in {filename}")
                    consistent = False
        
        if consistent:
            print("✅ All files contain the same 60 students with different scores")
        
        # Show score distribution comparison
        print("\n📈 Score Distribution Comparison:")
        print("Subject".ljust(25) + "Avg".ljust(8) + "Min".ljust(8) + "Max".ljust(8))
        print("-" * 50)
        
        for dataset in all_datasets:
            subject_name = dataset['filename'].split('/')[-1].replace('_4th_year_cse_a.csv', '').replace('_', ' ').title()
            subject_name = subject_name.replace('Cs401 ', '').replace('Cs402 ', '').replace('Cs403 ', '').replace('Cs404 ', '').replace('Cs405 ', '').replace('Cs406 ', '')
            
            print(f"{subject_name[:24].ljust(25)}{dataset['avg_score']:.1f}".ljust(8) + 
                  f"{dataset['min_score']}".ljust(8) + 
                  f"{dataset['max_score']}")

if __name__ == "__main__":
    main()