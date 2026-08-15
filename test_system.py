import unittest
import os
import json
import shutil
from student import Student
from student_manager import StudentManager
from file_handler import FileHandler
from validators import (
    validate_student_id, validate_age, validate_email,
    validate_phone, validate_cgpa, validate_semester
)

class TestStudentManagementSystem(unittest.TestCase):
    def setUp(self):
        # Set up a test directory and file path
        self.test_dir = os.path.join(os.path.dirname(__file__), "test_data")
        self.test_file = os.path.join(self.test_dir, "test_students.json")
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        
        # Initialize student manager with test file
        # Use relative path prefix to let StudentManager construct path cleanly
        self.manager = StudentManager(data_file="test_data/test_students.json")

    def tearDown(self):
        # Clean up test directories
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_add_valid_student(self):
        s = Student(
            student_id="STU101", name="Alice Smith", age=20, gender="Female",
            course="B.Tech", branch="CSE", semester=3, email="alice@test.com",
            phone="9876543210", address="123 Main St", cgpa=9.2
        )
        self.manager.add_student(s)
        self.assertIn("STU101", self.manager.students)
        self.assertEqual(self.manager.students["STU101"].name, "Alice Smith")

    def test_add_duplicate_student(self):
        s1 = Student(
            student_id="STU101", name="Alice Smith", age=20, gender="Female",
            course="B.Tech", branch="CSE", semester=3, email="alice@test.com",
            phone="9876543210", address="123 Main St", cgpa=9.2
        )
        self.manager.add_student(s1)
        
        s2 = Student(
            student_id="STU101", name="Bob Jones", age=21, gender="Male",
            course="B.Tech", branch="ECE", semester=3, email="bob@test.com",
            phone="9876543211", address="456 Main St", cgpa=8.5
        )
        with self.assertRaises(ValueError):
            self.manager.add_student(s2)

    def test_search_existing_student(self):
        s = Student(
            student_id="STU101", name="Alice Smith", age=20, gender="Female",
            course="B.Tech", branch="CSE", semester=3, email="alice@test.com",
            phone="9876543210", address="123 Main St", cgpa=9.2
        )
        self.manager.add_student(s)
        found = self.manager.search_by_id("STU101")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Alice Smith")

    def test_search_non_existing_student(self):
        found = self.manager.search_by_id("STU999")
        self.assertIsNone(found)

    def test_update_student(self):
        s = Student(
            student_id="STU101", name="Alice Smith", age=20, gender="Female",
            course="B.Tech", branch="CSE", semester=3, email="alice@test.com",
            phone="9876543210", address="123 Main St", cgpa=9.2
        )
        self.manager.add_student(s)
        
        self.manager.update_student("STU101", name="Alice Johnson", cgpa=9.5)
        updated = self.manager.search_by_id("STU101")
        self.assertEqual(updated.name, "Alice Johnson")
        self.assertEqual(updated.cgpa, 9.5)
        # Verify age remains unchanged
        self.assertEqual(updated.age, 20)

    def test_delete_student(self):
        s = Student(
            student_id="STU101", name="Alice Smith", age=20, gender="Female",
            course="B.Tech", branch="CSE", semester=3, email="alice@test.com",
            phone="9876543210", address="123 Main St", cgpa=9.2
        )
        self.manager.add_student(s)
        success = self.manager.delete_student("STU101")
        self.assertTrue(success)
        self.assertNotIn("STU101", self.manager.students)

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            validate_email("invalid-email")
        with self.assertRaises(ValueError):
            validate_email("alice@test")
        with self.assertRaises(ValueError):
            validate_email("")

    def test_invalid_cgpa(self):
        with self.assertRaises(ValueError):
            validate_cgpa("abc")
        with self.assertRaises(ValueError):
            validate_cgpa(11.0)
        with self.assertRaises(ValueError):
            validate_cgpa(-1.0)

    def test_corrupted_file_handling(self):
        # Write random non-JSON bytes to file
        with open(self.test_file, "w") as f:
            f.write("corrupted data")
        
        handler = FileHandler(self.test_file)
        with self.assertRaises(IOError):
            handler.load_data()

if __name__ == "__main__":
    unittest.main()
