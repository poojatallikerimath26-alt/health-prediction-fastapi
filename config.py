"""Loads settings from a local .env file (never committed) into environment variables."""
import os
from pathlib import Path


def load_env():
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        if value:  # a blank line such as "GEMINI_API_KEY=" must not hide a real value
            os.environ.setdefault(key.strip(), value)
