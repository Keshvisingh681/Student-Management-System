import sys
from student import Student
from student_manager import StudentManager
from validators import (
    validate_student_id, validate_age, validate_email,
    validate_phone, validate_cgpa, validate_semester, validate_required
)

def print_header(title):
    print("\n" + "=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50)

def display_student_detail(s):
    """Utility to print a single student record in detailed list view."""
    print(f"ID         : {s.student_id}")
    print(f"Name       : {s.name}")
    print(f"Age        : {s.age}")
    print(f"Gender     : {s.gender}")
    print(f"Course     : {s.course}")
    print(f"Branch     : {s.branch}")
    print(f"Semester   : {s.semester}")
    print(f"Email      : {s.email}")
    print(f"Phone      : {s.phone}")
    print(f"Address    : {s.address}")
    print(f"CGPA/Marks : {s.cgpa}")
    print("-" * 50)

def print_students_table(student_list):
    """Utility to print a list of students in a clean table format."""
    if not student_list:
        print("No student records found.")
        return

    # Table Header
    print(f"{'ID':<10} | {'Name':<20} | {'Course':<10} | {'Branch':<10} | {'Sem':<5} | {'CGPA':<5}")
    print("-" * 72)
    for s in student_list:
        name_trunc = s.name[:20] if len(s.name) > 20 else s.name
        course_trunc = s.course[:10] if len(s.course) > 10 else s.course
        branch_trunc = s.branch[:10] if len(s.branch) > 10 else s.branch
        print(f"{s.student_id:<10} | {name_trunc:<20} | {course_trunc:<10} | {branch_trunc:<10} | {s.semester:<5} | {s.cgpa:<5.2f}")
    print("-" * 72)
    print(f"Total Records: {len(student_list)}")

def get_input(prompt, validator_fn=None, default=None):
    """Prompts for input, validates it, or returns default if input is empty."""
    while True:
        try:
            val = input(prompt).strip()
            if not val:
                if default is not None:
                    return default
                else:
                    raise ValueError("Input cannot be empty. Please enter a value.")
            
            if validator_fn:
                return validator_fn(val)
            return val
        except ValueError as e:
            print(f"Validation Error: {e}")

def add_student_flow(manager):
    print_header("ADD NEW STUDENT")
    try:
        student_id = get_input("Enter Student ID (alphanumeric, 3-15 chars): ", validate_student_id)
        if manager.search_by_id(student_id):
            print(f"Error: Student with ID '{student_id}' already exists!")
            return

        name = get_input("Enter Student Name: ", lambda x: validate_required(x, "Name"))
        age = get_input("Enter Age (16-100): ", validate_age)
        gender = get_input("Enter Gender (Male/Female/Other): ", lambda x: validate_required(x, "Gender"))
        course = get_input("Enter Course (e.g. B.Tech, BSC): ", lambda x: validate_required(x, "Course"))
        branch = get_input("Enter Branch (e.g. CSE, ECE): ", lambda x: validate_required(x, "Branch"))
        semester = get_input("Enter Semester (1-8): ", validate_semester)
        email = get_input("Enter Email: ", validate_email)
        phone = get_input("Enter Phone Number: ", validate_phone)
        address = get_input("Enter Address: ", lambda x: validate_required(x, "Address"))
        cgpa = get_input("Enter Marks/CGPA (0.0-10.0): ", validate_cgpa)

        new_student = Student(
            student_id=student_id, name=name, age=age, gender=gender,
            course=course, branch=branch, semester=semester, email=email,
            phone=phone, address=address, cgpa=cgpa
        )
        manager.add_student(new_student)
        print("\nSuccess: Student added successfully!")
    except Exception as e:
        print(f"\nError creating student: {e}")

def view_all_students_flow(manager):
    print_header("ALL STUDENT RECORDS")
    students = manager.get_all_students()
    print_students_table(students)

def search_student_flow(manager):
    print_header("SEARCH STUDENT")
    print("1. Search by Student ID")
    print("2. Search by Name")
    print("3. Search by Course/Branch")
    choice = input("Enter search option (1-3): ").strip()

    if choice == '1':
        s_id = input("Enter Student ID to search: ").strip()
        s = manager.search_by_id(s_id)
        if s:
            print("\nStudent Record Found:")
            print("-" * 50)
            display_student_detail(s)
        else:
            print(f"No student found with ID '{s_id}'")
    elif choice == '2':
        name = input("Enter student name or part of name: ").strip()
        results = manager.search_by_name(name)
        print_students_table(results)
    elif choice == '3':
        query = input("Enter course or branch: ").strip()
        results = manager.search_by_course_or_branch(query)
        print_students_table(results)
    else:
        print("Invalid search choice!")

def update_student_flow(manager):
    print_header("UPDATE STUDENT INFORMATION")
    s_id = input("Enter Student ID to update: ").strip()
    student = manager.search_by_id(s_id)
    if not student:
        print(f"Error: Student with ID '{s_id}' not found.")
        return

    print("\nStudent Current Record found. Enter new value or press [Enter] to keep unchanged.")
    print("-" * 50)
    
    # We pass default current values to keep them if user presses Enter
    try:
        name = get_input(f"Name [{student.name}]: ", lambda x: validate_required(x, "Name"), default=student.name)
        age = get_input(f"Age [{student.age}]: ", validate_age, default=student.age)
        gender = get_input(f"Gender [{student.gender}]: ", lambda x: validate_required(x, "Gender"), default=student.gender)
        course = get_input(f"Course [{student.course}]: ", lambda x: validate_required(x, "Course"), default=student.course)
        branch = get_input(f"Branch [{student.branch}]: ", lambda x: validate_required(x, "Branch"), default=student.branch)
        semester = get_input(f"Semester [{student.semester}]: ", validate_semester, default=student.semester)
        email = get_input(f"Email [{student.email}]: ", validate_email, default=student.email)
        phone = get_input(f"Phone [{student.phone}]: ", validate_phone, default=student.phone)
        address = get_input(f"Address [{student.address}]: ", lambda x: validate_required(x, "Address"), default=student.address)
        cgpa = get_input(f"CGPA/Marks [{student.cgpa}]: ", validate_cgpa, default=student.cgpa)

        manager.update_student(
            student_id=s_id, name=name, age=age, gender=gender,
            course=course, branch=branch, semester=semester, email=email,
            phone=phone, address=address, cgpa=cgpa
        )
        print("\nSuccess: Student record updated successfully!")
    except Exception as e:
        print(f"\nError updating student: {e}")

def delete_student_flow(manager):
    print_header("DELETE STUDENT RECORD")
    s_id = input("Enter Student ID to delete: ").strip()
    student = manager.search_by_id(s_id)
    if not student:
        print(f"Error: Student with ID '{s_id}' not found.")
        return

    display_student_detail(student)
    confirm = input("Are you sure you want to delete this record? (yes/no): ").strip().lower()
    if confirm in ('y', 'yes'):
        if manager.delete_student(s_id):
            print("\nSuccess: Student record deleted successfully!")
        else:
            print("\nError: Could not delete record.")
    else:
        print("\nDeletion cancelled.")

def filter_students_flow(manager):
    print_header("FILTER STUDENTS")
    print("Provide values to filter by (or press Enter to skip):")
    branch = input("Branch: ").strip() or None
    course = input("Course: ").strip() or None
    semester = input("Semester: ").strip() or None
    min_cgpa = input("Minimum CGPA/Marks: ").strip() or None
    max_cgpa = input("Maximum CGPA/Marks: ").strip() or None

    results = manager.filter_students(
        branch=branch, course=course, semester=semester,
        min_cgpa=min_cgpa, max_cgpa=max_cgpa
    )
    print("\nFilter Results:")
    print_students_table(results)

def main():
    try:
        manager = StudentManager()
    except Exception as e:
        print(f"Fatal Startup Error: Could not initialize system data: {e}")
        sys.exit(1)

    while True:
        print_header("STUDENT MANAGEMENT SYSTEM")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Filter Students")
        print("7. Launch Graphical User Interface (GUI)")
        print("8. Exit")
        print("=" * 50)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            add_student_flow(manager)
        elif choice == '2':
            view_all_students_flow(manager)
        elif choice == '3':
            search_student_flow(manager)
        elif choice == '4':
            update_student_flow(manager)
        elif choice == '5':
            delete_student_flow(manager)
        elif choice == '6':
            filter_students_flow(manager)
        elif choice == '7':
            print("\nLaunching Graphical Interface...")
            try:
                import gui
                gui.main()
            except Exception as e:
                print(f"Failed to launch GUI: {e}")
        elif choice == '8':
            print("\nThank you for using the Student Management System. Exiting...")
            break
        else:
            print("\nInvalid choice! Please select an option between 1 and 8.")
            input("Press [Enter] to continue...")

if __name__ == "__main__":
    main()
