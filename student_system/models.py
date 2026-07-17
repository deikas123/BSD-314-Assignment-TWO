"""
models.py
OOP classes: Person, Student, Course, PerformanceAnalyzer
"""


class Person:
    """Base class representing a person in the university system."""

    def __init__(self, name, age, gender):
        # private attributes
        self._name = name
        self._age = age
        self._gender = gender

    # getters and setters
    def get_name(self):
        return self._name

    def set_name(self, name):
        if name and name.strip():
            self._name = name.strip()
        else:
            raise ValueError("Name cannot be empty")

    def get_age(self):
        return self._age

    def set_age(self, age):
        if age > 0:
            self._age = age
        else:
            raise ValueError("Age must be positive")

    def get_gender(self):
        return self._gender

    def display_info(self):
        """Display basic person info."""
        return f"Name: {self._name}, Age: {self._age}, Gender: {self._gender}"

    def __str__(self):
        return self.display_info()


class Student(Person):
    """Student class - inherits from Person."""

    def __init__(self, student_id, name, age, gender, course, year):
        # Call parent constructor
        super().__init__(name, age, gender)
        self._student_id = student_id
        self._course = course
        self._year = year
        self._marks = {}  # dictionary: subject -> score

    def get_student_id(self):
        return self._student_id

    def get_course(self):
        return self._course

    def set_course(self, course):
        self._course = course

    def get_year(self):
        return self._year

    def set_year(self, year):
        if year >= 1:
            self._year = year
        else:
            raise ValueError("Year must be at least 1")

    def get_marks(self):
        return self._marks

    def add_mark(self, subject, score):
        """Add or update a mark for a subject."""
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100")
        self._marks[subject] = score

    def calculate_average(self):
        """Calculate average of all marks."""
        if not self._marks:
            return 0.0
        total = sum(self._marks.values())
        return round(total / len(self._marks), 2)

    def compute_grade(self, average=None):
        """Compute letter grade based on average."""
        avg = average if average is not None else self.calculate_average()
        if avg >= 70:
            return "A"
        elif avg >= 60:
            return "B"
        elif avg >= 50:
            return "C"
        elif avg >= 40:
            return "D"
        else:
            return "E"

    def display_info(self):
        """Show student details including marks and grade."""
        base = super().display_info()
        avg = self.calculate_average()
        grade = self.compute_grade(avg)
        return (
            f"{base}\n"
            f"Student ID: {self._student_id}\n"
            f"Course: {self._course}\n"
            f"Year: {self._year}\n"
            f"Average: {avg}\n"
            f"Grade: {grade}"
        )

    def to_dict(self):
        """Convert student object to dictionary for file storage."""
        return {
            "student_id": self._student_id,
            "name": self._name,
            "age": self._age,
            "gender": self._gender,
            "course": self._course,
            "year": self._year,
            "marks": self._marks,
        }

    @classmethod
    def from_dict(cls, data):
        """Create Student object from dictionary."""
        student = cls(
            data["student_id"],
            data["name"],
            int(data["age"]),
            data["gender"],
            data["course"],
            int(data["year"]),
        )
        marks = data.get("marks", {})
        if isinstance(marks, dict):
            student._marks = marks
        return student


class Course:
    """Represents an academic course/unit offered by the university."""

    def __init__(self, course_code, course_name, credit_hours):
        self._course_code = course_code
        self._course_name = course_name
        self._credit_hours = credit_hours

    def get_course_code(self):
        return self._course_code

    def get_course_name(self):
        return self._course_name

    def get_credit_hours(self):
        return self._credit_hours

    def display_info(self):
        return (
            f"Code: {self._course_code}, "
            f"Name: {self._course_name}, "
            f"Credits: {self._credit_hours}"
        )

    def __str__(self):
        return self.display_info()


class PerformanceAnalyzer:
    """
    Analyzes student performance data.
    Works with Student objects (composition relationship).
    """

    GRADE_SCALE = ("A", "B", "C", "D", "E")  # tuple

    def __init__(self, students=None):
        # List of Student objects
        self._students = students if students is not None else []

    def add_student(self, student):
        self._students.append(student)

    def get_students(self):
        return self._students

    def class_average(self):
        """Compute overall class average."""
        if not self._students:
            return 0.0
        totals = [s.calculate_average() for s in self._students if s.get_marks()]
        if not totals:
            return 0.0
        return round(sum(totals) / len(totals), 2)

    def top_performer(self):
        """Return student with highest average."""
        scored = [s for s in self._students if s.get_marks()]
        if not scored:
            return None
        return max(scored, key=lambda s: s.calculate_average())

    def grade_distribution(self):
        """Return dictionary of grade counts."""
        distribution = {g: 0 for g in self.GRADE_SCALE}
        for student in self._students:
            if student.get_marks():
                grade = student.compute_grade()
                distribution[grade] = distribution.get(grade, 0) + 1
        return distribution

    def students_needing_support(self, threshold=50):
        """Return list of students below the pass threshold."""
        weak = []
        for student in self._students:
            if student.get_marks() and student.calculate_average() < threshold:
                weak.append(student)
        return weak

    def generate_report(self):
        """Generate a summary performance report as a string."""
        lines = [
            "=" * 50,
            "PERFORMANCE ANALYSIS REPORT",
            "=" * 50,
            f"Total Students: {len(self._students)}",
            f"Class Average: {self.class_average()}",
        ]
        top = self.top_performer()
        if top:
            lines.append(
                f"Top Performer: {top.get_name()} "
                f"({top.calculate_average()})"
            )
        lines.append("\nGrade Distribution:")
        for grade, count in self.grade_distribution().items():
            lines.append(f"  Grade {grade}: {count}")
        lines.append("=" * 50)
        return "\n".join(lines)
