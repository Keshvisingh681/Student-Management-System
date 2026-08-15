import re

def validate_required(value, field_name="Field"):
    """Validates that a field is not empty."""
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError(f"{field_name} is required and cannot be empty.")
    return str(value).strip()

def validate_student_id(student_id):
    """Validates student ID (alphanumeric, 3-15 chars)."""
    validate_required(student_id, "Student ID")
    s_id = str(student_id).strip()
    if not re.match(r"^[a-zA-Z0-9\-]{3,15}$", s_id):
        raise ValueError("Invalid Student ID. Must be 3-15 alphanumeric characters or hyphens.")
    return s_id

def validate_age(age):
    """Validates that age is an integer between 16 and 100."""
    try:
        age_val = int(age)
    except (ValueError, TypeError):
        raise ValueError("Age must be a valid integer.")
    if age_val < 16 or age_val > 100:
        raise ValueError("Age must be between 16 and 100.")
    return age_val

def validate_email(email):
    """Validates email format using regex."""
    validate_required(email, "Email")
    email_str = str(email).strip().lower()
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email_str):
        raise ValueError("Invalid email format. E.g., student@example.com")
    return email_str

def validate_phone(phone):
    """Validates phone number (10-15 digits, optional + prefix)."""
    validate_required(phone, "Phone Number")
    phone_str = str(phone).strip()
    phone_regex = r"^\+?[0-9]{10,15}$"
    if not re.match(phone_regex, phone_str):
        raise ValueError("Invalid phone number. Must be 10-15 digits, optional leading '+'.")
    return phone_str

def validate_cgpa(cgpa):
    """Validates CGPA / Marks (float between 0.0 and 10.0)."""
    try:
        cgpa_val = float(cgpa)
    except (ValueError, TypeError):
        raise ValueError("CGPA/Marks must be a valid number.")
    if cgpa_val < 0.0 or cgpa_val > 10.0:
        raise ValueError("CGPA/Marks must be between 0.0 and 10.0.")
    return cgpa_val

def validate_semester(semester):
    """Validates that semester is an integer between 1 and 8."""
    try:
        sem_val = int(semester)
    except (ValueError, TypeError):
        raise ValueError("Semester must be a valid integer.")
    if sem_val < 1 or sem_val > 8:
        raise ValueError("Semester must be between 1 and 8.")
    return sem_val
