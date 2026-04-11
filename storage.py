"""
storage.py — Handles saving complaint analyses to a CSV log file.
             The CSV format is compatible with Google Sheets import.
"""

import csv
import os

from config import DEFAULT_CSV

CSV_FIELDNAMES = [
    "date_submitted",
    "student_name",
    "complaint_text",
    "severity",
    "category",
    "law_name",
    "law_description",
    "law_confidence",
    "recommended_action",
    "ai_response",
]


def save_to_csv(
    result: dict,
    student_name: str,
    complaint_text: str,
    date_submitted: str,
    filepath: str = DEFAULT_CSV,
) -> None:
    """
    Append one complaint analysis as a new row in a CSV file.

    Creates the file with a header row if it does not yet exist.

    Args:
        result:          Parsed analysis dict from analyzer.analyze_complaint().
        student_name:    Student's full name.
        complaint_text:  Original complaint text.
        date_submitted:  ISO date string (YYYY-MM-DD).
        filepath:        Path to the CSV file (default: complaints_log.csv).
    """
    file_exists = os.path.isfile(filepath)
    law = result["applicable_law"]

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "date_submitted":   date_submitted,
                "student_name":     student_name,
                "complaint_text":   complaint_text,
                "severity":         result["severity"],
                "category":         result["category"],
                "law_name":         law["law_name"],
                "law_description":  law["description"],
                "law_confidence":   law["confidence"],
                "recommended_action": result["recommended_action"],
                "ai_response":      result["ai_response"],
            }
        )


def load_from_csv(filepath: str = DEFAULT_CSV) -> list[dict]:
    """
    Read all complaint records from an existing CSV log.

    Returns:
        List of row dicts, or an empty list if the file does not exist.
    """
    if not os.path.isfile(filepath):
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))