"""Calls the Google Gemini API to produce the Remarks (health risk prediction)."""
import json
import os
import time
import urllib.request
from datetime import date

UNAVAILABLE = "AI prediction unavailable"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class AIError(Exception):
    """Raised when the AI service cannot return a prediction."""


def age_from_dob(dob_text):
    day, month, year = (int(part) for part in dob_text.split("/"))
    today = date.today()
    return today.year - year - ((today.month, today.day) < (month, day))


def build_prompt(patient):
    return (
        "You are a screening assistant inside a health app. "
        f"Patient age: {age_from_dob(patient['dob'])} years (sex not provided, so use general adult reference ranges). "
        f"Blood test results: glucose {patient['glucose']} mg/dL, haemoglobin {patient['haemoglobin']} g/dL, "
        f"total cholesterol {patient['cholesterol']} mg/dL. "
        "In at most two short sentences, state the most likely health condition or risk these values suggest "
        "(for example diabetes risk, anaemia, high cholesterol, or no concern) and name which values are outside "
        "the normal range. Plain text only, no markdown. "
        "End with: Screening estimate only, not a diagnosis."
    )


def get_remarks(patient):
    """Return the prediction text for a validated patient dict."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise AIError("GEMINI_API_KEY is not set")

    model = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
    timeout = int(os.getenv("AI_TIMEOUT", "20"))
    body = json.dumps({
        "contents": [{"parts": [{"text": build_prompt(patient)}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 400},
    }).encode()

    last_error = "no response"
    for attempt in range(2):  # one retry for a slow or busy moment
        try:
            request = urllib.request.Request(
                API_URL.format(model=model),
                data=body,
                headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = json.load(response)
            text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            if text:
                return text
            last_error = "empty response"
        except Exception as error:
            last_error = str(error)
            if attempt == 0:
                time.sleep(1.5)
    raise AIError(last_error)
