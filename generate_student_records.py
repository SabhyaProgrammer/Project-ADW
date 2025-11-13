import json
import random

# Sample anime-inspired names
# ...existing code with first_names and last_names...

# Initialize the data structure
school_data = {}

# Generate data for each grade
for grade in range(1, 11):
    grade_name = f"Grade {grade}"
    school_data[grade_name] = {}
    
    # Generate data for each classroom using A-E naming
    for letter in 'ABCDE':
        class_name = f"Classroom {grade}{letter}"
        school_data[grade_name][class_name] = {}
        
        # Generate 20 students per classroom
        for student_num in range(20):
            # Create unique student name
            first = first_names[student_num % len(first_names)]
            last = last_names[student_num % len(last_names)]
            student_name = f"{first} {last} {student_num + 1}"
            
            # Define performance categories
            performance_type = random.choices(
                ['excellent', 'good', 'average', 'poor', 'failing'],
                weights=[10, 20, 40, 20, 10]  # Distribution percentages
            )[0]
            
            # Generate marks based on performance category
            def generate_mark(base):
                if performance_type == 'excellent':
                    return str(random.randint(85, 99))
                elif performance_type == 'good':
                    return str(random.randint(70, 84))
                elif performance_type == 'average':
                    return str(random.randint(50, 69))
                elif performance_type == 'poor':
                    return str(random.randint(35, 49))
                else:  # failing
                    return str(random.randint(20, 34))
            
            # Generate marks for each subject with realistic variation
            student_marks = {
                "English": generate_mark(60),
                "Maths": generate_mark(55),
                "Science": generate_mark(65),
                "Social Science": generate_mark(50),
                "Hindi": generate_mark(45)
            }
            
            school_data[grade_name][class_name][student_name] = student_marks

# Save the generated data to a JSON file
with open('student_records.json', 'w', encoding='utf-8') as f:
    json.dump(school_data, f, indent=4, ensure_ascii=False)

print("Anime-themed student records generated successfully!")
print("Total grades:", len(school_data))
print("Total classrooms:", len(school_data) * 5)
print("Total students:", len(school_data) * 5 * 20)
print("\nStudent performance distribution:")
print("- Excellent (85-99): 10%")
print("- Good (70-84): 20%")
print("- Average (50-69): 40%")
print("- Poor (35-49): 20%")
print("- Failing (20-34): 10%")