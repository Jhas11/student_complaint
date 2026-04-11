"""
display.py — Formats and prints the analysis report to the terminal.
"""

from config import SEVERITY_COLORS, RESET, SEPARATOR


def _wrap(text: str, width: int = 56, indent: str = "    ") -> str:
    """Word-wrap text to `width` chars, prefixing each line with `indent`."""
    words = text.split()
    lines, line = [], ""
    for word in words:
        if len(line) + len(word) + 1 > width:
            lines.append(indent + line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        lines.append(indent + line)
    return "\n".join(lines)


def print_analysis(result: dict, student_name: str, date_submitted: str) -> None:
    """Pretty-print a complaint analysis report to stdout."""
    sev = result["severity"]
    color = SEVERITY_COLORS.get(sev, "")
    law = result["applicable_law"]

    print(f"\n{SEPARATOR}")
    print("  COMPLAINT ANALYSIS REPORT")
    print(f"  Student : {student_name}   |   Date: {date_submitted}")
    print(SEPARATOR)
    print(f"  Severity   : {color}{sev}{RESET}")
    print(f"  Category   : {result['category']}")
    print(SEPARATOR)
    print("  Applicable Law")
    print(f"    Name        : {law['law_name']}")
    print(f"    Description : {law['description']}")
    print(f"    Confidence  : {law['confidence']}")
    print(SEPARATOR)
    print("  Recommended Action")
    print(_wrap(result["recommended_action"]))
    print(SEPARATOR)
    print("  AI Response to Student")
    print(_wrap(result["ai_response"]))
    print(f"{SEPARATOR}\n")


def print_header() -> None:
    """Print the app banner."""
    print("\n╔══════════════════════════════════════════════╗")
    print("║   Student Complaint Analyzer — Philippines  ║")
    print("╚══════════════════════════════════════════════╝\n")


def print_error(message: str) -> None:
    """Print a formatted error message."""
    print(f"\n  \033[91m✗ Error:\033[0m {message}\n")


def print_success(message: str) -> None:
    """Print a formatted success message."""
    print(f"  \033[92m✓\033[0m {message}")