"""
analyzer.py — Sends the complaint to OpenRouter and returns parsed results.

OpenRouter is an API gateway that gives access to many free models.
It uses the OpenAI-compatible format.

Install:
    pip install openai

Get a free API key at:
    https://openrouter.ai -> Sign In -> Keys -> Create Key
"""

import json
import os
from openai import OpenAI

from config import MODEL, BASE_URL
from prompt import build_prompt


def analyze_complaint(
    student_name: str,
    complaint_text: str,
    date_submitted: str,
    api_key: str | None = None,
) -> dict:
    """
    Call OpenRouter with the complaint prompt and return a parsed analysis dict.

    Args:
        student_name:    Full name of the student filing the complaint.
        complaint_text:  The complaint description.
        date_submitted:  ISO date string (YYYY-MM-DD).
        api_key:         Optional API key; falls back to OPENROUTER_API_KEY env var.

    Returns:
        dict with keys: severity, category, applicable_law,
                        recommended_action, ai_response.

    Raises:
        ValueError:           If no API key is found.
        json.JSONDecodeError: If the model returns malformed JSON.
    """
    key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise ValueError(
            "No API key found. Set the OPENROUTER_API_KEY environment variable "
            "or pass api_key= to analyze_complaint()."
        )

    client = OpenAI(
        api_key=key,
        base_url=BASE_URL,
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

    # Strip markdown fences if the model wraps the JSON in ```
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw.strip())