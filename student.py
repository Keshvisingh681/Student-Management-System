from validators import (
    validate_student_id, validate_required, validate_age,
    validate_email, validate_phone, validate_cgpa, validate_semester
)

class Person:
    """Base class representing a person with general details."""
    def __init__(self, name, age, gender, email, phone, address):
        self.name = validate_required(name, "Name")
        self.age = validate_age(age)
        self.gender = validate_required(gender, "Gender")
        self.email = validate_email(email)
        self.phone = validate_phone(phone)
        self.address = validate_required(address, "Address")

    def to_dict(self):
        """Convert person object to dictionary structure."""
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "email": self.email,
            "phone": self.phone,
            "address": self.address
        }


class Student(Person):
    """Student class representing a college student, inheriting from Person."""
    def __init__(self, student_id, name, age, gender, course, branch, semester, email, phone, address, cgpa):
        # Call base class constructor
        super().__init__(name, age, gender, email, phone, address)
        self.student_id = validate_student_id(student_id)
        self.course = validate_required(course, "Course")
        self.branch = validate_required(branch, "Branch")
        self.semester = validate_semester(semester)
        self.cgpa = validate_cgpa(cgpa)

    def to_dict(self):
        """Convert student object and parent attributes to dictionary structure."""
        data = super().to_dict()
        data.update({
            "student_id": self.student_id,
            "course": self.course,
            "branch": self.branch,
            "semester": self.semester,
            "cgpa": self.cgpa
        })
        return data

    @classmethod
    def from_dict(cls, data):
        """Create a Student instance from a dictionary."""
        return cls(
            student_id=data.get("student_id"),
            name=data.get("name"),
            age=data.get("age"),
            gender=data.get("gender"),
            course=data.get("course"),
            branch=data.get("branch"),
            semester=data.get("semester"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            cgpa=data.get("cgpa")
        )

    def update_info(self, **kwargs):
        """Update student attributes with validation. Unprovided fields remain unchanged."""
        if "name" in kwargs and kwargs["name"]:
            self.name = validate_required(kwargs["name"], "Name")
        if "age" in kwargs and kwargs["age"]:
            self.age = validate_age(kwargs["age"])
        if "gender" in kwargs and kwargs["gender"]:
            self.gender = validate_required(kwargs["gender"], "Gender")
        if "course" in kwargs and kwargs["course"]:
            self.course = validate_required(kwargs["course"], "Course")
        if "branch" in kwargs and kwargs["branch"]:
            self.branch = validate_required(kwargs["branch"], "Branch")
        if "semester" in kwargs and kwargs["semester"]:
            self.semester = validate_semester(kwargs["semester"])
        if "email" in kwargs and kwargs["email"]:
            self.email = validate_email(kwargs["email"])
        if "phone" in kwargs and kwargs["phone"]:
            self.phone = validate_phone(kwargs["phone"])
        if "address" in kwargs and kwargs["address"]:
            self.address = validate_required(kwargs["address"], "Address")
        if "cgpa" in kwargs and kwargs["cgpa"]:
            self.cgpa = validate_cgpa(kwargs["cgpa"])

    def __str__(self):
        return f"Student[ID={self.student_id}, Name={self.name}, Course={self.course}, CGPA={self.cgpa}]"
