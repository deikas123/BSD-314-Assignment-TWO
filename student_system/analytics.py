"""
analytics.py
Data cleaning and statistical analysis using Pandas and NumPy.
"""

import os

import numpy as np
import pandas as pd

from student_system.file_handler import DATA_DIR, MARKS_CSV, STUDENTS_CSV


def load_students_dataframe():
    """Load students CSV into a pandas DataFrame."""
    if not os.path.exists(STUDENTS_CSV):
        return pd.DataFrame()
    try:
        df = pd.read_csv(STUDENTS_CSV)
        return df
    except Exception as e:
        print(f"Error loading students CSV: {e}")
        return pd.DataFrame()


def load_marks_dataframe():
    """Load marks CSV into a pandas DataFrame."""
    if not os.path.exists(MARKS_CSV):
        return pd.DataFrame()
    try:
        df = pd.read_csv(MARKS_CSV)
        return df
    except Exception as e:
        print(f"Error loading marks CSV: {e}")
        return pd.DataFrame()


def clean_data(df):
    """
    (a) Data Cleaning
    - Detect missing values
    - Remove duplicates
    - Validate records
    Returns cleaned DataFrame and a report dictionary.
    """
    report = {
        "original_rows": len(df),
        "missing_before": {},
        "duplicates_removed": 0,
        "invalid_removed": 0,
        "final_rows": 0,
    }

    if df.empty:
        report["final_rows"] = 0
        return df, report

    # Detect missing values
    report["missing_before"] = df.isnull().sum().to_dict()

    # Work on a copy
    cleaned = df.copy()

    # For marks data: drop rows where score is missing/empty
    if "score" in cleaned.columns:
        # Convert score to numeric, invalid become NaN
        cleaned["score"] = pd.to_numeric(cleaned["score"], errors="coerce")
        before = len(cleaned)
        cleaned = cleaned.dropna(subset=["score"])
        report["invalid_removed"] += before - len(cleaned)

        # Validate score range 0-100
        before = len(cleaned)
        cleaned = cleaned[(cleaned["score"] >= 0) & (cleaned["score"] <= 100)]
        report["invalid_removed"] += before - len(cleaned)

    # Remove empty subject rows if present
    if "subject" in cleaned.columns:
        cleaned = cleaned[cleaned["subject"].notna() & (cleaned["subject"] != "")]

    # Remove duplicates
    before = len(cleaned)
    if "student_id" in cleaned.columns and "subject" in cleaned.columns:
        cleaned = cleaned.drop_duplicates(subset=["student_id", "subject"], keep="last")
    else:
        cleaned = cleaned.drop_duplicates()
    report["duplicates_removed"] = before - len(cleaned)

    # Validate age if present
    if "age" in cleaned.columns:
        cleaned["age"] = pd.to_numeric(cleaned["age"], errors="coerce")
        before = len(cleaned)
        cleaned = cleaned[(cleaned["age"] > 0) & (cleaned["age"] < 100)]
        report["invalid_removed"] += before - len(cleaned)

    cleaned = cleaned.reset_index(drop=True)
    report["final_rows"] = len(cleaned)
    return cleaned, report


def compute_statistics(marks_df):
    """
    (b) Statistical Analysis using NumPy and Pandas
    Compute mean, median, mode, std, max, min.
    """
    stats = {}

    if marks_df.empty or "score" not in marks_df.columns:
        return {
            "mean": None,
            "median": None,
            "mode": None,
            "std_dev": None,
            "maximum": None,
            "minimum": None,
            "count": 0,
        }

    scores = marks_df["score"].dropna().values
    if len(scores) == 0:
        return {
            "mean": None,
            "median": None,
            "mode": None,
            "std_dev": None,
            "maximum": None,
            "minimum": None,
            "count": 0,
        }

    stats["count"] = len(scores)
    stats["mean"] = round(float(np.mean(scores)), 2)
    stats["median"] = round(float(np.median(scores)), 2)
    stats["std_dev"] = round(float(np.std(scores)), 2)
    stats["maximum"] = float(np.max(scores))
    stats["minimum"] = float(np.min(scores))

    # Mode using pandas
    mode_series = marks_df["score"].mode()
    if len(mode_series) > 0:
        stats["mode"] = float(mode_series.iloc[0])
    else:
        stats["mode"] = None

    # Per-subject statistics
    if "subject" in marks_df.columns:
        subject_stats = (
            marks_df.groupby("subject")["score"]
            .agg(["mean", "median", "std", "max", "min", "count"])
            .round(2)
        )
        stats["by_subject"] = subject_stats.to_dict()

    # Per-student averages
    if "student_id" in marks_df.columns:
        student_avg = (
            marks_df.groupby(["student_id", "name"])["score"]
            .mean()
            .round(2)
            .reset_index()
        )
        student_avg.columns = ["student_id", "name", "average"]
        stats["by_student"] = student_avg.to_dict(orient="records")

    return stats


def format_cleaning_report(report):
    """Format cleaning report as readable text."""
    lines = [
        "--- DATA CLEANING REPORT ---",
        f"Original rows      : {report['original_rows']}",
        f"Missing values     : {report['missing_before']}",
        f"Duplicates removed : {report['duplicates_removed']}",
        f"Invalid removed    : {report['invalid_removed']}",
        f"Final clean rows   : {report['final_rows']}",
    ]
    return "\n".join(lines)


def format_statistics(stats):
    """Format statistics as readable text."""
    if stats.get("count", 0) == 0:
        return "No score data available for statistical analysis."

    lines = [
        "--- STATISTICAL ANALYSIS ---",
        f"Number of scores : {stats['count']}",
        f"Mean             : {stats['mean']}",
        f"Median           : {stats['median']}",
        f"Mode             : {stats['mode']}",
        f"Std Deviation    : {stats['std_dev']}",
        f"Maximum Score    : {stats['maximum']}",
        f"Minimum Score    : {stats['minimum']}",
    ]
    return "\n".join(lines)


def run_full_analysis():
    """Run cleaning + statistics and return results."""
    marks_df = load_marks_dataframe()
    cleaned, clean_report = clean_data(marks_df)
    stats = compute_statistics(cleaned)

    # Save cleaned data
    cleaned_path = os.path.join(DATA_DIR, "marks_cleaned.csv")
    try:
        if not cleaned.empty:
            cleaned.to_csv(cleaned_path, index=False)
    except IOError as e:
        print(f"Could not save cleaned data: {e}")

    return cleaned, clean_report, stats
