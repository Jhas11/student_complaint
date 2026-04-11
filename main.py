"""
main.py — Entry point for the Student Complaint Analyzer.

Run:
    python main.py

Environment:
    ANTHROPIC_API_KEY  — your Anthropic API key (required)
"""

import json

from analyzer import analyze_complaint
from display  import print_header, print_analysis, print_error, print_success
from storage  import save_to_csv
from cli      import prompt_required, prompt_date, prompt_yes_no, prompt_filename


def run_once() -> None:
    """Collect one complaint, analyze it, display it, and optionally save it."""
    print("\n  — New complaint —")
    student_name    = prompt_required("Student name")
    complaint_text  = prompt_required("Complaint description")
    date_submitted  = prompt_date()

    print("\n  Analyzing complaint...\n")

    try:
        result = analyze_complaint(student_name, complaint_text, date_submitted)
    except ValueError as e:
        print_error(str(e))
        return
    except json.JSONDecodeError:
        print_error("Could not parse the AI response as JSON. Please try again.")
        return
    except Exception as e:
        print_error(str(e))
        return

    print_analysis(result, student_name, date_submitted)

    if prompt_yes_no("Save to CSV log?"):
        filepath = prompt_filename("  CSV filename")
        save_to_csv(result, student_name, complaint_text, date_submitted, filepath)
        print_success(f"Saved to {filepath}")


def main() -> None:
    print_header()
    while True:
        run_once()
        if not prompt_yes_no("\n  Analyze another complaint?", default="n"):
            print("\n  Goodbye.\n")
            break


if __name__ == "__main__":
    main()