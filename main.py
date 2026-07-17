"""
main.py
BSD 314 - Student Performance Analytics and Management System
Menu-driven console application.

Run: python main.py
"""

import os
import sys

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from student_system.student_manager import StudentManager
from student_system.academic_manager import AcademicManager, SUBJECTS
from student_system.models import Course, Person, Student, PerformanceAnalyzer
from student_system import analytics
from student_system import visualization


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def print_header(title):
    print("\n" + "=" * 55)
    print(f"  {title}")
    print("=" * 55)


def main_menu():
    print_header("STUDENT PERFORMANCE MANAGEMENT SYSTEM")
    print("  1. Student Management")
    print("  2. Academic Management")
    print("  3. Reports & Analytics")
    print("  4. Data Visualization")
    print("  5. OOP Example")
    print("  6. Export Technical Report (PDF)")
    print("  0. Exit")
    print("-" * 55)
    return input("Enter choice: ").strip()


def student_menu(sm):
    while True:
        print_header("STUDENT MANAGEMENT")
        print("  1. Register Student")
        print("  2. Update Student Information")
        print("  3. Delete Student")
        print("  4. Search Student")
        print("  5. Display All Students")
        print("  0. Back to Main Menu")
        print("-" * 55)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            print("\n--- Register Student ---")
            sid = input("Student ID: ").strip()
            name = input("Name: ").strip()
            age = input("Age: ").strip()
            gender = input("Gender (M/F): ").strip().upper()
            course = input("Course (e.g. BSc IT): ").strip()
            year = input("Year of Study: ").strip()
            ok, msg = sm.register_student(sid, name, age, gender, course, year)
            print(msg)

        elif choice == "2":
            print("\n--- Update Student ---")
            sid = input("Student ID to update: ").strip()
            print("(Leave blank to keep current value)")
            name = input("New Name: ").strip() or None
            age = input("New Age: ").strip() or None
            gender = input("New Gender: ").strip() or None
            course = input("New Course: ").strip() or None
            year = input("New Year: ").strip() or None
            ok, msg = sm.update_student(sid, name, age, gender, course, year)
            print(msg)

        elif choice == "3":
            print("\n--- Delete Student ---")
            sid = input("Student ID to delete: ").strip()
            confirm = input(f"Are you sure you want to delete {sid}? (y/n): ")
            if confirm.lower() == "y":
                ok, msg = sm.delete_student(sid)
                print(msg)
            else:
                print("Delete cancelled.")

        elif choice == "4":
            print("\n--- Search Student ---")
            print("  1. Search by ID")
            print("  2. Search by Name")
            sub = input("Choice: ").strip()
            if sub == "1":
                sid = input("Student ID: ").strip()
                student = sm.search_by_id(sid)
                if student:
                    print(student.display_info())
                else:
                    print("Student not found.")
            elif sub == "2":
                name = input("Name: ").strip()
                results = sm.search_by_name(name)
                if results:
                    for s in results:
                        print("-" * 40)
                        print(s.display_info())
                else:
                    print("No matching students found.")

        elif choice == "5":
            print("\n" + sm.display_all())

        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

        pause()


def academic_menu(am):
    while True:
        print_header("ACADEMIC MANAGEMENT")
        print("  1. Enter Marks")
        print("  2. Calculate Average")
        print("  3. Compute Grade")
        print("  4. Display Transcript")
        print("  0. Back to Main Menu")
        print("-" * 55)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            print("\n--- Enter Marks ---")
            sid = input("Student ID: ").strip()
            print("Available subjects:")
            for i, subj in enumerate(SUBJECTS, 1):
                print(f"  {i}. {subj}")
            print(f"  {len(SUBJECTS) + 1}. Other (custom)")
            sub_choice = input("Select subject number: ").strip()
            try:
                idx = int(sub_choice)
                if 1 <= idx <= len(SUBJECTS):
                    subject = SUBJECTS[idx - 1]
                else:
                    subject = input("Enter subject name: ").strip()
            except ValueError:
                subject = input("Enter subject name: ").strip()

            score = input(f"Score for {subject} (0-100): ").strip()
            ok, msg = am.enter_marks(sid, subject, score)
            print(msg)

        elif choice == "2":
            sid = input("Student ID: ").strip()
            avg, msg = am.calculate_average(sid)
            print(msg)

        elif choice == "3":
            sid = input("Student ID: ").strip()
            grade, msg = am.compute_grade(sid)
            print(msg)

        elif choice == "4":
            sid = input("Student ID: ").strip()
            print(am.display_transcript(sid))

        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

        pause()


def reports_menu(sm, am):
    while True:
        print_header("REPORTS & ANALYTICS")
        print("  1. Performance Analyzer Report")
        print("  2. Data Cleaning Report")
        print("  3. Statistical Analysis")
        print("  4. Run Full Analysis")
        print("  0. Back to Main Menu")
        print("-" * 55)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            analyzer = am.get_analyzer()
            print(analyzer.generate_report())
            weak = analyzer.students_needing_support()
            if weak:
                print("\nStudents needing academic support:")
                for s in weak:
                    print(f"  - {s.get_name()} (Avg: {s.calculate_average()})")

        elif choice == "2":
            marks_df = analytics.load_marks_dataframe()
            cleaned, report = analytics.clean_data(marks_df)
            print(analytics.format_cleaning_report(report))

        elif choice == "3":
            cleaned, clean_report, stats = analytics.run_full_analysis()
            print(analytics.format_statistics(stats))
            if stats.get("by_student"):
                print("\nPer-student averages:")
                for row in stats["by_student"]:
                    print(
                        f"  {row['student_id']}: {row['name']} -> {row['average']}"
                    )

        elif choice == "4":
            print("\nRunning full data analysis...")
            cleaned, clean_report, stats = analytics.run_full_analysis()
            print(analytics.format_cleaning_report(clean_report))
            print()
            print(analytics.format_statistics(stats))
            print("\n--- EVALUATION & RECOMMENDATIONS ---")
            if stats.get("mean") is not None:
                mean = stats["mean"]
                print(f"Class mean score is {mean}.")
                if mean < 50:
                    print("RECOMMENDATION: Overall performance is below average.")
                    print("  - Introduce remedial classes for weak subjects.")
                    print("  - Schedule peer tutoring sessions.")
                    print("  - Review teaching methods and assessment design.")
                elif mean < 65:
                    print("RECOMMENDATION: Performance is average.")
                    print("  - Provide extra practice materials.")
                    print("  - Identify and support students below 50%.")
                    print("  - Encourage group study and continuous assessment.")
                else:
                    print("RECOMMENDATION: Performance is good.")
                    print("  - Maintain current teaching strategies.")
                    print("  - Offer advanced challenges for top performers.")
                    print("  - Monitor students near the pass borderline.")

                if stats.get("std_dev") and stats["std_dev"] > 15:
                    print(
                        "NOTE: High standard deviation indicates wide performance gap."
                    )
                    print("  Consider differentiated instruction.")

        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

        pause()


def visualization_menu():
    print_header("DATA VISUALIZATION")
    print("Generating charts from marks data...")
    marks_df = analytics.load_marks_dataframe()
    cleaned, _ = analytics.clean_data(marks_df)

    if cleaned.empty:
        print("No marks data available. Enter marks first.")
        pause()
        return

    paths = visualization.generate_all_charts(cleaned)
    print(f"\n{len(paths)} chart(s) generated in outputs/charts/")
    print("Charts created:")
    print("  1. Bar Chart   - Average score by subject")
    print("  2. Histogram   - Distribution of scores")
    print("  3. Pie Chart   - Grade distribution")
    print("  4. Line Graph  - Student average scores")
    pause()


def demo_oop():
    """Show OOP features used in the project."""
    print_header("OOP EXAMPLE")

    print("\n1. INHERITANCE & CONSTRUCTORS")
    print("   Person -> Student")
    person = Person("Jane Doe", 20, "F")
    student = Student("STU001", "John Kamau", 21, "M", "BSc IT", 2)
    print(f"   Person:  {person}")
    print(f"   Student: {student.get_name()} ({student.get_student_id()})")

    print("\n2. ENCAPSULATION (getters/setters)")
    student.set_name("John K. Kamau")
    print(f"   Updated name via setter: {student.get_name()}")

    print("\n3. METHOD OVERRIDING (display_info)")
    print("   Person.display_info():")
    print(f"     {person.display_info()}")
    print("   Student.display_info() [overridden]:")
    student.add_mark("Programming", 78)
    student.add_mark("Mathematics", 65)
    print(student.display_info())

    print("\n4. POLYMORPHISM")
    people = [person, student]
    for p in people:
        # Same method name, different behaviour
        print(f"   -> {p.display_info().split(chr(10))[0]}")

    print("\n5. COURSE CLASS")
    course = Course("BSD314", "Programming in Python", 3)
    print(f"   {course}")

    print("\n6. PERFORMANCE ANALYZER")
    analyzer = PerformanceAnalyzer([student])
    print(analyzer.generate_report())
    pause()


def export_report_menu():
    print_header("EXPORT TECHNICAL REPORT")
    try:
        from export_report_pdf import main as export_pdf
        result = export_pdf()
        if result == 0:
            print("\nReport exported to report/Technical_Report.pdf")
        else:
            print("\nCould not create PDF. Check that report/Technical_Report.md exists.")
    except ImportError as e:
        print(f"\nMissing package for PDF export: {e}")
        print("Run: pip install markdown xhtml2pdf")
    except Exception as e:
        print(f"\nError exporting report: {e}")
    pause()


def seed_sample_data(sm, am):
    """Load sample students if the database is empty."""
    if len(sm.students) > 0:
        return

    print("No existing data found. Loading sample students...")
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
        sm.register_student(sid, name, age, gender, course, year)
        for subject, score in sample_marks[sid].items():
            am.enter_marks(sid, subject, score)

    print(f"Loaded {len(sample)} sample students with marks.")


def main():
    sm = StudentManager()
    am = AcademicManager(sm)

    # Ask whether to seed sample data
    if len(sm.students) == 0:
        ans = input("Database is empty. Load sample data for demo? (y/n): ").strip()
        if ans.lower() == "y":
            seed_sample_data(sm, am)

    while True:
        choice = main_menu()

        if choice == "1":
            student_menu(sm)
        elif choice == "2":
            academic_menu(am)
        elif choice == "3":
            reports_menu(sm, am)
        elif choice == "4":
            visualization_menu()
        elif choice == "5":
            demo_oop()
        elif choice == "6":
            export_report_menu()
        elif choice == "0":
            print("\nThank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            pause()


if __name__ == "__main__":
    main()
