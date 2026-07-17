"""
visualization.py
Generate charts using Matplotlib: bar, histogram, pie, line.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from student_system.file_handler import DATA_DIR

# Output folder for charts
CHARTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "outputs", "charts"
)


def ensure_charts_dir():
    os.makedirs(CHARTS_DIR, exist_ok=True)


def plot_bar_chart(marks_df, filename="bar_chart.png"):
    """Bar chart: average score per subject."""
    ensure_charts_dir()
    if marks_df.empty or "subject" not in marks_df.columns:
        print("No data for bar chart.")
        return None

    avg_by_subject = marks_df.groupby("subject")["score"].mean().sort_values()

    plt.figure(figsize=(9, 5))
    bars = plt.bar(avg_by_subject.index, avg_by_subject.values, color="steelblue")
    plt.title("Average Score by Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Score")
    plt.xticks(rotation=30, ha="right")
    plt.ylim(0, 100)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, filename)
    plt.savefig(path, dpi=120)
    plt.close()
    return path


def plot_histogram(marks_df, filename="histogram.png"):
    """Histogram: distribution of all scores."""
    ensure_charts_dir()
    if marks_df.empty or "score" not in marks_df.columns:
        print("No data for histogram.")
        return None

    scores = marks_df["score"].dropna()

    plt.figure(figsize=(8, 5))
    plt.hist(scores, bins=10, color="teal", edgecolor="black", alpha=0.75)
    plt.title("Distribution of Student Scores")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.axvline(
        scores.mean(),
        color="red",
        linestyle="--",
        label=f"Mean = {scores.mean():.1f}",
    )
    plt.legend()
    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, filename)
    plt.savefig(path, dpi=120)
    plt.close()
    return path


def plot_pie_chart(marks_df, filename="pie_chart.png"):
    """Pie chart: grade distribution."""
    ensure_charts_dir()
    if marks_df.empty or "score" not in marks_df.columns:
        print("No data for pie chart.")
        return None

    # Compute overall grade per student (average then grade)
    if "student_id" in marks_df.columns:
        avg = marks_df.groupby("student_id")["score"].mean()
    else:
        avg = marks_df["score"]

    def to_grade(score):
        if score >= 70:
            return "A"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C"
        elif score >= 40:
            return "D"
        else:
            return "E"

    grades = avg.apply(to_grade)
    counts = grades.value_counts().reindex(["A", "B", "C", "D", "E"], fill_value=0)
    # Only show grades that exist
    counts = counts[counts > 0]

    colors = ["#2ecc71", "#3498db", "#f1c40f", "#e67e22", "#e74c3c"]
    plt.figure(figsize=(7, 7))
    plt.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors[: len(counts)],
    )
    plt.title("Grade Distribution")
    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, filename)
    plt.savefig(path, dpi=120)
    plt.close()
    return path


def plot_line_graph(marks_df, filename="line_graph.png"):
    """Line graph: student averages ranked / or subject comparison."""
    ensure_charts_dir()
    if marks_df.empty:
        print("No data for line graph.")
        return None

    if "student_id" in marks_df.columns and "name" in marks_df.columns:
        student_avg = (
            marks_df.groupby("name")["score"].mean().sort_values().reset_index()
        )
        plt.figure(figsize=(10, 5))
        plt.plot(
            student_avg["name"],
            student_avg["score"],
            marker="o",
            linestyle="-",
            color="darkorange",
        )
        plt.title("Student Average Scores (Ranked)")
        plt.xlabel("Student")
        plt.ylabel("Average Score")
        plt.xticks(rotation=40, ha="right")
        plt.ylim(0, 100)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
    else:
        # Fallback: line of scores
        scores = marks_df["score"].dropna().values
        plt.figure(figsize=(8, 5))
        plt.plot(range(len(scores)), scores, marker="o")
        plt.title("Score Trend")
        plt.xlabel("Record Index")
        plt.ylabel("Score")
        plt.tight_layout()

    path = os.path.join(CHARTS_DIR, filename)
    plt.savefig(path, dpi=120)
    plt.close()
    return path


def generate_all_charts(marks_df):
    """Generate all four required visualizations. Returns list of paths."""
    paths = []
    for func in (plot_bar_chart, plot_histogram, plot_pie_chart, plot_line_graph):
        path = func(marks_df)
        if path:
            paths.append(path)
            print(f"Saved: {path}")
    return paths
