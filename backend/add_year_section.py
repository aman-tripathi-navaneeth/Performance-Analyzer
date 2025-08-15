#!/usr/bin/env python3

def add_year_section_to_response():
    """Add year_section_distribution to the response"""
    
    # Read the file
    with open('app/api/analytics.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the line with 'year_distribution': year_distribution, and add after it
    for i, line in enumerate(lines):
        if "'year_distribution': year_distribution," in line:
            # Insert the new line after this one
            indent = line[:len(line) - len(line.lstrip())]  # Get the indentation
            new_line = f"{indent}'year_section_distribution': year_section_distribution,\n"
            lines.insert(i + 1, new_line)
            break
    
    # Write back to file
    with open('app/api/analytics.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Added year_section_distribution to response")

if __name__ == "__main__":
    add_year_section_to_response()