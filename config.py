MODEL = "openrouter/auto"
BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_CSV = "complaints_log.csv"

PHILIPPINE_LAWS = [
    "Anti-Bullying Act of 2013 (RA 10627)",
    "Safe Spaces Act (RA 11313)",
    "Child Protection Policy (DepEd Order No. 40, s. 2012)",
    "Data Privacy Act of 2012 (RA 10173)",
    "Anti-Sexual Harassment Act (RA 7877)",
]

SEVERITY_COLORS = {
    "LOW":    "\033[92m",
    "MEDIUM": "\033[93m",
    "HIGH":   "\033[91m",
}
RESET = "\033[0m"
SEPARATOR = "─" * 60
