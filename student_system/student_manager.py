"""
student_manager.py
Handles student CRUD operations using lists and dictionaries.
"""

from student_system.models import Student
from student_system import file_handler


class StudentManager:
    """Manages registration, update, delete, search and display of students."""

    def __init__(self):
        self.students = []  # list of Student objects
        self._load_from_file()

    def _load_from_file(self):
        """Load existing students from JSON storage."""
        data = file_handler.load_students_json()
        self.students = []
        for item in data:
            try:
                self.students.append(Student.from_dict(item))
            except (KeyError, ValueError, TypeError) as e:
                print(f"Skipping invalid record: {e}")

    def _save(self):
        """Persist all students to files."""
        data = [s.to_dict() for s in self.students]
        file_handler.export_all(data)

    def register_student(self, student_id, name, age, gender, course, year):
        """Register a new student. Returns (success, message)."""
        # Check for duplicate ID
        if self.search_by_id(student_id) is not None:
            return False, f"Student ID {student_id} already exists."

        try:
            student = Student(student_id, name, int(age), gender, course, int(year))
            self.students.append(student)
            self._save()
            return True, f"Student {name} registered successfully."
        except ValueError as e:
            return False, str(e)

    def update_student(self, student_id, name=None, age=None, gender=None,
                       course=None, year=None):
        """Update student information. Returns (success, message)."""
        student = self.search_by_id(student_id)
        if student is None:
            return False, f"Student ID {student_id} not found."

        try:
            if name:
                student.set_name(name)
            if age is not None:
                student.set_age(int(age))
            if gender:
                student._gender = gender
            if course:
                student.set_course(course)
            if year is not None:
                student.set_year(int(year))
            self._save()
            return True, f"Student {student_id} updated successfully."
        except ValueError as e:
            return False, str(e)

    def delete_student(self, student_id):
        """Delete a student by ID. Returns (success, message)."""
        student = self.search_by_id(student_id)
        if student is None:
            return False, f"Student ID {student_id} not found."

        self.students.remove(student)
        self._save()
        return True, f"Student {student_id} deleted successfully."

    def search_by_id(self, student_id):
        """Search for a student by ID. Returns Student or None."""
        for student in self.students:
            if student.get_student_id() == student_id:
                return student
        return None

    def search_by_name(self, name):
        """Search students by name (partial, case-insensitive). Returns list."""
        results = []
        name_lower = name.lower()
        for student in self.students:
            if name_lower in student.get_name().lower():
                results.append(student)
        return results

    def display_all(self):
        """Return formatted string of all students."""
        if not self.students:
            return "No students registered yet."

        lines = [
            "-" * 70,
            f"{'ID':<12}{'Name':<20}{'Age':<6}{'Gender':<10}{'Course':<15}{'Year':<6}",
            "-" * 70,
        ]
        for s in self.students:
            lines.append(
                f"{s.get_student_id():<12}"
                f"{s.get_name():<20}"
                f"{s.get_age():<6}"
                f"{s.get_gender():<10}"
                f"{s.get_course():<15}"
                f"{s.get_year():<6}"
            )
        lines.append("-" * 70)
        lines.append(f"Total students: {len(self.students)}")
        return "\n".join(lines)

    def get_all_dicts(self):
        """Return list of student dictionaries."""
        return [s.to_dict() for s in self.students]
