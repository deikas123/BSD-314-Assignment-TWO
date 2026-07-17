"""
run_demo.py
Loads sample data and runs analysis + chart generation for testing.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from student_system.student_manager import StudentManager
from student_system.academic_manager import AcademicManager
from student_system.models import Person, Student, Course, PerformanceAnalyzer
from student_system import analytics
from student_system import visualization


def seed(sm, am):
    sample = [
        ("STU001", "Alice Wanjiku", 20, "F", "BSc IT", 2),
        ("STU002", "Brian Otieno", 22, "M", "BSc IT", 2),
        ("STU003", "Carol Njeri", 19, "F", "BSc CS", 1),
        ("STU004", "David Mwangi", 21, "M", "BSc IT", 3),
        ("STU005", "Esther Akinyi", 20, "F", "BSc CS", 2),
        ("STU006", "Frank Kiprop", 23, "M", "BSc IT", 3),
        ("STU007", "Grace Muthoni", 21, "F", "BSc CS", 2),
        ("STU008", "Hassan Ali", 22, "M", "BSc IT", 1),
    ]
    sample_marks = {
        "STU001": {"Mathematics": 72, "Programming": 85, "Database": 78, "Networking": 70, "Web Development": 80},
        "STU002": {"Mathematics": 55, "Programming": 60, "Database": 58, "Networking": 52, "Web Development": 65},
        "STU003": {"Mathematics": 88, "Programming": 90, "Database": 85, "Networking": 82, "Web Development": 91},
        "STU004": {"Mathematics": 45, "Programming": 50, "Database": 42, "Networking": 48, "Web Development": 55},
        "STU005": {"Mathematics": 67, "Programming": 72, "Database": 70, "Networking": 65, "Web Development": 74},
        "STU006": {"Mathematics": 38, "Programming": 40, "Database": 35, "Networking": 42, "Web Development": 45},
        "STU007": {"Mathematics": 75, "Programming": 80, "Database": 77, "Networking": 73, "Web Development": 82},
        "STU008": {"Mathematics": 60, "Programming": 55, "Database": 62, "Networking": 58, "Web Development": 64},
    }

    for sid, name, age, gender, course, year in sample:
        if sm.search_by_id(sid) is None:
            sm.register_student(sid, name, age, gender, course, year)
        for subject, score in sample_marks[sid].items():
            am.enter_marks(sid, subject, score)

    print(f"Sample data loaded ({len(sm.students)} students)")


def main():
    print("=" * 55)
    print("  Student Performance System - Test Run")
    print("=" * 55)

    sm = StudentManager()
    am = AcademicManager(sm)
    seed(sm, am)

    print("\n--- Display Students ---")
    print(sm.display_all())

    print("\n--- Sample Transcript (STU001) ---")
    print(am.display_transcript("STU001"))

    print("\n--- Performance Report ---")
    analyzer = am.get_analyzer()
    print(analyzer.generate_report())

    print("\n--- Data Cleaning & Statistics ---")
    cleaned, clean_report, stats = analytics.run_full_analysis()
    print(analytics.format_cleaning_report(clean_report))
    print()
    print(analytics.format_statistics(stats))

    print("\n--- Generating Visualizations ---")
    paths = visualization.generate_all_charts(cleaned)
    print(f"Generated {len(paths)} charts")

    print("\n--- OOP Example ---")
    p = Person("Test Person", 25, "M")
    s = Student("STU009", "Sample Student", 20, "F", "BSc IT", 1)
    s.add_mark("Programming", 75)
    c = Course("BSD314", "Programming in Python", 3)
    print(f"Person: {p.display_info()}")
    print(f"Student:\n{s.display_info()}")
    print(f"Course: {c}")

    print("\n" + "=" * 55)
    print("  TEST RUN COMPLETE")
    print("=" * 55)


if __name__ == "__main__":
    main()
