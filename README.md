# Student Management System

A modular, user-friendly console-based **Student Management System** built with Python. Developed as a college project, this application showcases key Object-Oriented Programming (OOP) concepts, comprehensive CRUD operations, robust validation patterns, custom exception handling, and persistent data storage.

---

## Features
- **Add Student**: Save detailed records including ID, Name, Age, Gender, Course, Branch, Semester, Email, Phone, Address, and CGPA.
- **View Records**: Clean table-formatted list of all student details.
- **Search Engine**: Search by Student ID, Name, or Course/Branch (with case-insensitive matching).
- **Update Records**: Edit specific information while preserving unprovided/blank details.
- **Delete Records**: Safely delete files with user confirmation.
- **Multi-Filter**: Filter records by branch, course, semester, and CGPA range.
- **Data Persistence**: Automatic JSON saving and parsing with error check capabilities.
- **Robust Validation**: Real-time format validation for email, phone numbers, CGPA, and age limit.

## Technologies Used
- **Language**: Python 3.x
- **Storage format**: JSON (JavaScript Object Notation)
- **Standard Libraries**: `json`, `os`, `re`, `sys`, `unittest`

## OOP Concepts Used
1. **Inheritance**: The system models entities cleanly by inheriting `Student` from a base `Person` class.
2. **Encapsulation**: Attributes are protected and managed through constructor validations and update methods.
3. **Abstraction**: Low-level database operations (file read/write) are abstracted away behind the `FileHandler` class interface.
4. **Polymorphism**: The `to_dict()` serialization method is overridden in the subclasses to build comprehensive JSON structures.

## Project Structure
```text
student-management-system/
│
├── main.py              # Main application loop and CLI menus
├── student.py           # Person and Student domain model classes
├── student_manager.py   # Student database business logic (CRUD/Filters)
├── file_handler.py      # Abstracted reading, writing, and file verification
├── validators.py        # Input format validation functions
├── test_system.py       # Diagnostic test runner suite
├── requirements.txt     # Dependency definition
├── .gitignore           # File/Directory ignore definition
│
├── data/
│   └── students.json    # Persistent JSON storage database
│
└── report/
    └── Project_Report.md # Detailed Academic Project Report
```

## Installation Instructions
1. Ensure Python 3.8+ is installed on your local computer.
2. Clone or extract this project folder to your local working directory.
3. Open a terminal or Command Prompt inside the directory.

## How to Run
Execute the main script via Python:
```bash
python main.py
```

### Running Tests
Execute the unit testing framework file:
```bash
python -m unittest test_system.py
```

## Exception Handling
The system handles:
- **Duplicate ID**: Prevents registering a student under an already existing ID.
- **Invalid Email**: Rejects addresses missing `@` or domain details.
- **Invalid CGPA**: Validates values to ensure they reside between `0.0` and `10.0`.
- **Invalid Semester & Age**: Confirms valid integer ranges (1-8 for semesters, 16-100 for age).
- **Corrupted File**: Catches JSON parser failures and warns the user without crashing.

## Sample Usage
```text
==================================================
            STUDENT MANAGEMENT SYSTEM
==================================================
1. Add Student
2. View All Students
3. Search Student
4. Update Student
5. Delete Student
6. Filter Students
7. Exit
==================================================
Enter your choice: 1

==================================================
                 ADD NEW STUDENT
==================================================
Enter Student ID: STU101
Enter Student Name: Alice Smith
Enter Age (16-100): 20
Enter Gender: Female
Enter Course: B.Tech
Enter Branch: CSE
Enter Semester: 3
Enter Email: alice@example.com
Enter Phone Number: 9876543210
Enter Address: 123 University Ave
Enter Marks/CGPA: 9.5

Success: Student added successfully!
```

## Future Enhancements
- GUI Interface build using Tkinter.
- Relational Database backend using SQLite/PostgreSQL.
- CSV report generator export features.

## License
This project is licensed under the MIT License.
