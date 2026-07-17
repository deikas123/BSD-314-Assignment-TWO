"""
file_handler.py
Handles reading and writing student data to CSV and JSON files.
Includes exception handling for file operations.
"""

import csv
import json
import os


# Default file paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
STUDENTS_JSON = os.path.join(DATA_DIR, "students.json")
STUDENTS_CSV = os.path.join(DATA_DIR, "students.csv")
MARKS_CSV = os.path.join(DATA_DIR, "marks.csv")


def ensure_data_dir():
    """Create data directory if it does not exist."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
    except OSError as e:
        print(f"Error creating data directory: {e}")


def save_students_json(students_list):
    """
    Save list of student dictionaries to JSON file.
    students_list: list of dicts from Student.to_dict()
    """
    ensure_data_dir()
    try:
        with open(STUDENTS_JSON, "w", encoding="utf-8") as f:
            json.dump(students_list, f, indent=4)
        return True
    except (IOError, TypeError) as e:
        print(f"Error saving JSON: {e}")
        return False


def load_students_json():
    """Load student data from JSON file. Returns list of dicts."""
    ensure_data_dir()
    if not os.path.exists(STUDENTS_JSON):
        return []
    try:
        with open(STUDENTS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading JSON: {e}")
        return []


def save_students_csv(students_list):
    """Save basic student info to CSV (without nested marks)."""
    ensure_data_dir()
    try:
        with open(STUDENTS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["student_id", "name", "age", "gender", "course", "year"]
            )
            for s in students_list:
                writer.writerow(
                    [
                        s.get("student_id", ""),
                        s.get("name", ""),
                        s.get("age", ""),
                        s.get("gender", ""),
                        s.get("course", ""),
                        s.get("year", ""),
                    ]
                )
        return True
    except IOError as e:
        print(f"Error saving CSV: {e}")
        return False


def save_marks_csv(students_list):
    """Save marks as flat CSV rows: student_id, subject, score."""
    ensure_data_dir()
    try:
        with open(MARKS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "name", "subject", "score"])
            for s in students_list:
                marks = s.get("marks", {})
                if marks:
                    for subject, score in marks.items():
                        writer.writerow(
                            [
                                s.get("student_id", ""),
                                s.get("name", ""),
                                subject,
                                score,
                            ]
                        )
                else:
                    # Still record student with empty mark for analytics
                    writer.writerow(
                        [s.get("student_id", ""), s.get("name", ""), "", ""]
                    )
        return True
    except IOError as e:
        print(f"Error saving marks CSV: {e}")
        return False


def export_all(students_list):
    """Export student data to both JSON and CSV formats."""
    ok_json = save_students_json(students_list)
    ok_csv = save_students_csv(students_list)
    ok_marks = save_marks_csv(students_list)
    return ok_json and ok_csv and ok_marks
