# Student Management System - Entering the Battlefield

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

A robust, Python-based command-line interface (CLI) application designed to manage student academic records efficiently. This system allows educators and administrators to track student performance across multiple grades and classrooms, providing real-time insights into class averages and individual student status.

## 🚀 Features

*   **Comprehensive Grade Management**: Support for **Grade 1 through Grade 10**.
*   **Classroom Organization**: Each grade is divided into **5 Classrooms (A, B, C, D, E)** for granular management.
*   **Subject Tracking**: Records marks for core subjects:
    *   English
    *   Maths
    *   Science
    *   Social Science
    *   Hindi
*   **Automated Analytics**:
    *   Calculates **Class Averages** dynamically.
    *   Determines student status: **Pass**, **Fail**, or **Tie** based on the class average.
*   **CRUD Operations**:
    *   **Add**: Register new students and enter their marks.
    *   **View**: Display detailed class reports with student rankings and status.
    *   **Edit**: Update student names or modify marks for specific subjects.
*   **Data Persistence**: All records are automatically saved to `student_records.json`, ensuring no data is lost between sessions.
*   **Sample Data Generator**: Includes a utility script to generate realistic sample data for testing and demonstration purposes.

## 📋 Prerequisites

*   **Python 3.6+**: Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

## 🛠️ Installation

1.  **Clone the Repository** (or download the source code):
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Verify Files**:
    Ensure the following files are present in the directory:
    *   `Ch10 Mini project - Entering the Battlefield.py`
    *   `generate_student_records.py`

## 💻 Usage

### 1. Initialize with Sample Data (Optional)
If you want to start with a populated database (10 Grades, 50 Classrooms, 1000 Students), run the generator script first:

```bash
python generate_student_records.py
```
*This will create a `student_records.json` file with anime-themed student names and realistic mark distributions.*

### 2. Run the Application
Start the main management system:

```bash
python "Ch10 Mini project - Entering the Battlefield.py"
```

### 3. Navigation Guide
Follow the on-screen prompts to navigate the system:

1.  **Select Grade**: Choose a grade from 1 to 10.
2.  **Select Classroom**: Choose a classroom (e.g., Classroom 1A, 1B...).
3.  **Choose Action**:
    *   `Add`: Enter a new student's name and their marks for all subjects.
    *   `View`: See a list of all students in the selected class, their total marks, and their Pass/Fail status relative to the class average.
    *   `Edit`: Modify an existing student's name or update their marks for a specific subject.
    *   `Exit`: Save changes and quit the application.

## 📂 Project Structure

```text
.
├── Ch10 Mini project - Entering the Battlefield.py  # Main Application Entry Point
├── generate_student_records.py                      # Sample Data Generator Script
└── student_records.json                             # JSON Database (Auto-generated)
```

## 🔍 Technical Details

*   **Data Storage**: The application uses a nested JSON structure (`Grade -> Classroom -> Student -> Subject -> Marks`) for efficient data retrieval and storage.
*   **Error Handling**: Robust error handling ensures the application doesn't crash on invalid inputs (e.g., non-numeric marks, out-of-range selections).
*   **Statistics Logic**:
    *   **Class Average**: Total Marks of all students / (Number of Students * Number of Subjects).
    *   **Pass/Fail**: A student passes if their total marks > class average.

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements or bug fixes, please feel free to:
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

## 📄 License

This project is open-source and available for personal and educational use.

---
*Built with ❤️ using Python.*
