"""
academic_manager.py
Handles marks entry, average calculation, grade computation and transcripts.
"""

from student_system.models import PerformanceAnalyzer


# Subject list used in the system (tuple - immutable)
SUBJECTS = ("Mathematics", "Programming", "Database", "Networking", "Web Development")


class AcademicManager:
    """Manages academic operations for registered students."""

    def __init__(self, student_manager):
        self.student_manager = student_manager

    def enter_marks(self, student_id, subject, score):
        """Enter marks for a student. Returns (success, message)."""
        student = self.student_manager.search_by_id(student_id)
        if student is None:
            return False, f"Student ID {student_id} not found."

        try:
            score = float(score)
            student.add_mark(subject, score)
            self.student_manager._save()
            return True, f"Mark {score} recorded for {subject}."
        except ValueError as e:
            return False, str(e)

    def calculate_average(self, student_id):
        """Calculate and return average for a student."""
        student = self.student_manager.search_by_id(student_id)
        if student is None:
            return None, f"Student ID {student_id} not found."
        if not student.get_marks():
            return None, "No marks recorded for this student."
        avg = student.calculate_average()
        return avg, f"Average for {student.get_name()}: {avg}"

    def compute_grade(self, student_id):
        """Compute grade for a student. Returns (grade, message)."""
        student = self.student_manager.search_by_id(student_id)
        if student is None:
            return None, f"Student ID {student_id} not found."
        if not student.get_marks():
            return None, "No marks recorded for this student."
        grade = student.compute_grade()
        avg = student.calculate_average()
        return grade, f"Grade for {student.get_name()}: {grade} (Average: {avg})"

    def display_transcript(self, student_id):
        """Generate a formatted academic transcript."""
        student = self.student_manager.search_by_id(student_id)
        if student is None:
            return f"Student ID {student_id} not found."

        marks = student.get_marks()
        lines = [
            "=" * 50,
            "           ACADEMIC TRANSCRIPT",
            "=" * 50,
            f"Student ID : {student.get_student_id()}",
            f"Name       : {student.get_name()}",
            f"Course     : {student.get_course()}",
            f"Year       : {student.get_year()}",
            "-" * 50,
            f"{'Subject':<25}{'Score':<10}{'Grade':<10}",
            "-" * 50,
        ]

        if not marks:
            lines.append("No marks recorded.")
        else:
            for subject, score in marks.items():
                # Compute grade per subject
                if score >= 70:
                    g = "A"
                elif score >= 60:
                    g = "B"
                elif score >= 50:
                    g = "C"
                elif score >= 40:
                    g = "D"
                else:
                    g = "E"
                lines.append(f"{subject:<25}{score:<10}{g:<10}")

            avg = student.calculate_average()
            overall = student.compute_grade(avg)
            lines.append("-" * 50)
            lines.append(f"Average    : {avg}")
            lines.append(f"Overall Grade: {overall}")

        lines.append("=" * 50)
        return "\n".join(lines)

    def get_analyzer(self):
        """Return a PerformanceAnalyzer with current students."""
        return PerformanceAnalyzer(self.student_manager.students)
