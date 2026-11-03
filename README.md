# Health Prediction App

A small web app that stores patient blood-test records (glucose, haemoglobin, cholesterol) and uses the Google Gemini API to write a short screening remark for each record.

**Stack:** Python 3, FastAPI (backend), Jinja2 + Bootstrap 5 (frontend), SQLite (storage), Gemini REST API (AI remarks).

## Features
- Create, read, edit and delete records (CRUD)
- Validation: full name, email format, date of birth (dd/mm/yyyy, real calendar date, not in the future), numeric blood values within plausible ranges
- Duplicate detection (same name + date of birth + email)
- AI remarks generated on save; regenerated on edit only when the date of birth or blood values change
- If the AI service fails, the record is still saved with a note and a **Regenerate** button

## Project layout
| File | Purpose |
|---|---|
| `app.py` | FastAPI routes |
| `validators.py` | Input validation rules |
| `database.py` | SQLite access (parameterised queries) |
| `ai_client.py` | Gemini API call, prompt, timeout/retry |
| `config.py` | Loads settings from a local `.env` file |
| `templates/` | HTML pages (Bootstrap) |

## Setup
```
pip install -r requirements.txt
copy .env.example .env      (Windows)   |   cp .env.example .env   (Mac/Linux)
```
Open `.env` and put your own Gemini key after `GEMINI_API_KEY=` (free key from https://aistudio.google.com). The `.env` file is git-ignored and never uploaded.

## Run
```
python app.py
```
Then open http://127.0.0.1:8000

## Settings (environment or `.env`)
- `GEMINI_API_KEY` – required for AI remarks
- `GEMINI_MODEL` – default `gemini-3.1-flash-lite`
- `AI_TIMEOUT` – seconds, default 20
- `HEALTH_DB` – database file path, default `health.db`

## Notes
- Dates are stored and shown as dd/mm/yyyy. Input with `.` or `-` separators (e.g. 28.01.1960) is accepted and converted.
- Remarks are a screening estimate only and not medical advice.
