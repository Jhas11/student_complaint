"""
analyzer.py — Sends the complaint to OpenRouter and returns parsed results.
"""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

from config import MODEL, BASE_URL
from prompt import build_prompt


def analyze_complaint(
    student_name: str,
    complaint_text: str,
    date_submitted: str,
    api_key: str | None = None,
) -> dict:
    # Strip whitespace/newlines that can sneak in from .env files
    key = (api_key or os.environ.get("OPENROUTER_API_KEY") or "").strip()

    if not key:
        raise ValueError(
            "No API key found. Set the OPENROUTER_API_KEY environment variable "
            "or pass api_key= to analyze_complaint()."
        )

    # Show partial key so you can verify it loaded correctly
    print(f"  [debug] Key loaded: {key[:12]}...{key[-4:]}")

    if not key.startswith("sk-or-"):
        raise ValueError(
            f"API key looks wrong — expected it to start with 'sk-or-' "
            f"but got '{key[:12]}...'. "
            "Please copy the key again from https://openrouter.ai/settings/keys"
        )

    # OpenRouter requires these headers to identify your app
    client = OpenAI(
        api_key=key,
        base_url=BASE_URL,
        default_headers={
            "HTTP-Referer": "https://github.com/student-complaint-analyzer",
            "X-Title": "Student Complaint Analyzer",
        },
    )

    prompt = build_prompt(student_name, complaint_text, date_submitted)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a structured JSON API. "
                    "Always respond with valid JSON only. "
                    "No extra text, no markdown fences."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw.strip())
