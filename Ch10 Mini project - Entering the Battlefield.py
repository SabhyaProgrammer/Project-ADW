import json
import os
import sys

# explicit lists (no generator)
grades = [
    "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5",
    "Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10"
]

classrooms = [
    "Classroom A", "Classroom B", "Classroom C", "Classroom D", "Classroom E"
]

subjects = {
    "1": "English",
    "2": "Maths",
    "3": "Science",
    "4": "Social Science",
    "5": "Hindi"
}

DATA_FILE = "student_records.json"

def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # If already nested structure, return it
            if isinstance(data, dict) and any(k.startswith("Grade ") for k in data.keys()):
                return data
            # Legacy flat dict: put into Grade 1 / Class 1
            nested = {g: {c: {} for c in classrooms} for g in grades}
            if isinstance(data, dict):
                nested[grades[0]][classrooms[0]] = data
            return nested
        # No file: create empty nested structure
        return {g: {c: {} for c in classrooms} for g in grades}
    except Exception as e:
        print(f"Error loading data: {e}")
        return {g: {c: {} for c in classrooms} for g in grades}

def save_data(school_data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(school_data, f, indent=4)
        print("Data saved successfully!")
    except Exception as e:
        print(f"Error saving data: {e}")

def select_grade_classroom(school_data):
    while True:
        print("\nSelect Grade:")
        for idx, g in enumerate(grades, 1):
            print(f"{idx}. {g}")
        grade_choice = input("Enter grade number (or 0 to exit): ").strip()
        if grade_choice == "0":
            print("Exiting.")
            sys.exit(0)
        if not grade_choice.isdigit() or not (1 <= int(grade_choice) <= len(grades)):
            print("Invalid selection. Try again.")
            continue
        selected_grade = grades[int(grade_choice) - 1]
        grade_number = selected_grade.split()[1]  # Gets the number from "Grade X"

        print(f"\nSelect Classroom in {selected_grade}:")
        for idx, c in enumerate(classrooms, 1):
            classroom_label = f"Classroom {grade_number}{c.split()[1]}"  # Creates "XY" format
            print(f"{idx}. {classroom_label}")
        class_choice = input("Enter classroom number (or 0 to go back to grade selection): ").strip()
        if class_choice == "0":
            continue
        if not class_choice.isdigit() or not (1 <= int(class_choice) <= len(classrooms)):
            print("Invalid selection. Returning to grade selection.")
            continue
            
        base_classroom = classrooms[int(class_choice) - 1]
        selected_classroom = f"Classroom {grade_number}{base_classroom.split()[1]}"

        # ensure structure
        school_data.setdefault(selected_grade, {})
        if not all(f"Classroom {grade_number}{letter}" in school_data[selected_grade] 
                  for letter in "ABCDE"):
            school_data[selected_grade] = {
                f"Classroom {grade_number}{letter}": {} 
                for letter in "ABCDE"
            }

        return selected_grade, selected_classroom, school_data[selected_grade][selected_classroom]

def calculate_class_statistics(students):
    if not students:
        return 0.0, {}
    student_totals = {}
    total_marks = 0
    for name, subs in students.items():
        # only sum numeric marks
        student_sum = sum(int(v) for v in subs.values() if str(v).isdigit())
        student_totals[name] = student_sum
        total_marks += student_sum
    # average = total_marks / (number_of_students * number_of_subjects)
    # use total subjects count from subjects dict (5)
    class_average = total_marks / (len(students) * len(subjects)) if students else 0.0
    return class_average, student_totals

def display_students(current_grade, current_classroom, students):
    if not students:
        print("No students found.")
        return
    class_average, student_totals = calculate_class_statistics(students)
    print("\n=== Student Records ===")
    print(f"Class Average ({current_grade} - {current_classroom}): {class_average:.2f}\n")
    for name in sorted(students.keys()):
        print(f"Student: {name}")
        student_total = student_totals.get(name, 0)
        status = "Pass" if student_total > class_average else ("Fail" if student_total < class_average else "Tie")
        print(f"Status : {status}")
        print("-" * 30)
        for subj in subjects.values():
            marks = students[name].get(subj, "Not entered")
            print(f"{subj:<15}: {marks}")
        print(f"{'Total Marks':<15}: {student_total}")
        print("-" * 30)
    print("\n" + "=" * 40 + "\n")

def add_student(students):
    while True:
        student_name = input("Enter student name (0 for back): ").strip()
        if student_name == "0":
            return
        if not student_name:
            print("Name cannot be empty.")
            continue
        if student_name in students:
            print("Student already exists.")
            continue
        students[student_name] = {}
        print(f"{student_name} added.")
        entered_subjects = set()
        while True:
            remaining_subjects = {num: subj for num, subj in subjects.items() if subj not in entered_subjects}
            if not remaining_subjects:
                print("All subjects entered for this student.")
                return
            print("\nSelect subject:")
            for num, subj in remaining_subjects.items():
                print(f"{num}. {subj}")
            subject_choice = input("\nEnter subject serial number (0 for back): ")

            # New code block starts here
            subject_choice = input("\nEnter subject serial number (0 for back): ").strip()
            if subject_choice == "0":
                # remove student if user backs out before entering any marks
                if not students[student_name]:
                    students.pop(student_name, None)
                return
            if subject_choice not in remaining_subjects:
                print("Invalid subject selection.")
                continue
            subject_name = remaining_subjects[subject_choice]
            while True:
                marks = input(f"Enter marks for {subject_name} (0 for back): ").strip()
                if marks == "0":
                    break
                if not marks.isdigit():
                    print("Please enter numerical values only for marks.")
                    continue
                marks_int = int(marks)
                if marks_int < 0 or marks_int > 100:
                    print("Marks must be between 0 and 100.")
                    continue
                confirm = input("Type 'confirm' to save and continue, or 'back' to re-enter marks: ").strip().lower()
                if confirm == "back":
                    continue
                if confirm == "confirm":
                    students[student_name][subject_name] = str(marks_int)
                    entered_subjects.add(subject_name)
                    print(f"Marks for {subject_name} saved for {student_name}.")
                    break
                print("Invalid option.")

def edit_menu(students):
    if not students:
        print("No students found.")
        return
    print("\nStudent List:")
    student_list = list(students.keys())
    for idx, name in enumerate(student_list, 1):
        print(f"{idx}. {name}")
    choice = input("\nEnter student number to edit (0 for back): ").strip()
    if choice == "0":
        return
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(student_list):
        print("Invalid selection.")
        return
    student_name = student_list[int(choice) - 1]
    edit_choice = input("Type 'name' to edit name or 'marks' to edit marks: ").strip().lower()
    if edit_choice == "name":
        new_name = input("Enter new name: ").strip()
        if new_name:
            students[new_name] = students.pop(student_name)
            print(f"Student name updated to {new_name}.")
        else:
            print("Name cannot be empty.")
    elif edit_choice == "marks":
        print("\nSubjects and marks:")
        for subj in subjects.values():
            print(f"{subj}: {students[student_name].get(subj, 'Not entered')}")
        subject_to_edit = input("Enter subject name to edit marks: ").strip()
        if subject_to_edit in students[student_name]:
            while True:
                new_marks = input(f"Enter new marks for {subject_to_edit} (0 for back): ").strip()
                if new_marks == "0":
                    return
                if not new_marks.isdigit():
                    print("Please enter numerical values only.")
                    continue
                new_marks_int = int(new_marks)
                if new_marks_int < 0 or new_marks_int > 100:
                    print("Marks must be between 0 and 100.")
                    continue
                students[student_name][subject_to_edit] = str(new_marks_int)
                print(f"Marks for {subject_to_edit} updated to {new_marks_int}.")
                return
        else:
            print("Subject not found for this student.")
    else:
        print("Invalid choice.")

def main():
    school_data = load_data()
    # ask grade/classroom before showing menu
    current_grade, current_classroom, students = select_grade_classroom(school_data)

    while True:
        action = input('Choose Action : Add | View | Edit\n(Type "exit" to quit): ').strip().lower()
        if action == "add":
            add_student(students)
            save_data(school_data)
        elif action == "view":
            display_students(current_grade, current_classroom, students)
        elif action == "edit":
            edit_menu(students)
            save_data(school_data)
        elif action == "exit":
            save_data(school_data)
            break
        else:
            print("Invalid action. Please choose Add, View, Edit, or exit.")

if __name__ == "__main__":
    main()

































































































































































































































































































































































































































































































































































































































































































































































