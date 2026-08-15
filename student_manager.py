import os
from student import Student
from file_handler import FileHandler

class StudentManager:
    """Class responsible for student record logic (CRUD, Search, Filter)."""
    def __init__(self, data_file="data/students.json"):
        # Put path relative to the script execution or absolute path
        # Let's support relative path resolved cleanly
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, data_file)
        self.file_handler = FileHandler(self.file_path)
        self.students = {} # dictionary keyed by student_id
        self.load_students()

    def load_students(self):
        """Loads students from JSON file into local dictionary mapping."""
        try:
            raw_data = self.file_handler.load_data()
            self.students = {}
            for item in raw_data:
                student = Student.from_dict(item)
                self.students[student.student_id] = student
        except Exception as e:
            # Re-raise to let Main know
            raise e

    def save_students(self):
        """Saves current state of students dictionary back to JSON file."""
        data_list = [s.to_dict() for s in self.students.values()]
        self.file_handler.save_data(data_list)

    def add_student(self, student):
        """Adds a student record. Raises ValueError if student ID exists."""
        if student.student_id in self.students:
            raise ValueError(f"Student with ID '{student.student_id}' already exists.")
        self.students[student.student_id] = student
        self.save_students()

    def get_all_students(self):
        """Returns list of all Student objects."""
        return list(self.students.values())

    def search_by_id(self, student_id):
        """Searches for a student by ID. Returns Student object or None."""
        return self.students.get(student_id.strip())

    def search_by_name(self, name):
        """Searches for students by matching Name (case-insensitive substring match)."""
        query = name.strip().lower()
        return [s for s in self.students.values() if query in s.name.lower()]

    def search_by_course_or_branch(self, query):
        """Searches for students by course or branch (case-insensitive substring match)."""
        q = query.strip().lower()
        return [s for s in self.students.values() if q in s.course.lower() or q in s.branch.lower()]

    def update_student(self, student_id, **kwargs):
        """Updates an existing student's details and saves to disk."""
        student = self.search_by_id(student_id)
        if not student:
            raise ValueError(f"Student with ID '{student_id}' not found.")
        student.update_info(**kwargs)
        self.save_students()
        return student

    def delete_student(self, student_id):
        """Deletes student record. Returns True if deleted, False if not found."""
        s_id = student_id.strip()
        if s_id in self.students:
            del self.students[s_id]
            self.save_students()
            return True
        return False

    def filter_students(self, branch=None, course=None, semester=None, min_cgpa=None, max_cgpa=None):
        """Filters students by various criteria."""
        results = list(self.students.values())
        if branch:
            results = [s for s in results if branch.strip().lower() in s.branch.lower()]
        if course:
            results = [s for s in results if course.strip().lower() in s.course.lower()]
        if semester is not None:
            try:
                sem = int(semester)
                results = [s for s in results if s.semester == sem]
            except ValueError:
                pass
        if min_cgpa is not None:
            try:
                min_c = float(min_cgpa)
                results = [s for s in results if s.cgpa >= min_c]
            except ValueError:
                pass
        if max_cgpa is not None:
            try:
                max_c = float(max_cgpa)
                results = [s for s in results if s.cgpa <= max_c]
            except ValueError:
                pass
        return results
