"""
cli.py — Interactive command-line helpers for collecting user input.
"""

from datetime import date


def prompt(label: str, default: str = "") -> str:
    """
    Prompt the user for a value, showing an optional default.
    Returns the default if the user presses Enter without typing.
    """
    suffix = f" [{default}]" if default else ""
    return input(f"  {label}{suffix}: ").strip() or default


def prompt_required(label: str) -> str:
    """Keep prompting until the user enters a non-empty value."""
    while True:
        value = prompt(label)
        if value:
            return value
        print(f"    {label} is required.")


def prompt_date(label: str = "Date submitted (YYYY-MM-DD)") -> str:
    """Prompt for a date, defaulting to today."""
    today = date.today().isoformat()
    while True:
        value = prompt(label, default=today)
        try:
            date.fromisoformat(value)
            return value
        except ValueError:
            print("    Please enter a valid date in YYYY-MM-DD format.")


def prompt_yes_no(label: str, default: str = "y") -> bool:
    """Prompt for a yes/no answer. Returns True for yes."""
    options = "Y/n" if default == "y" else "y/N"
    answer = prompt(f"{label} ({options})").lower() or default
    return answer in ("y", "yes")


def prompt_filename(label: str, default: str = "complaints_log.csv") -> str:
    """Prompt for a filename, with a default."""
    return prompt(label, default=default)