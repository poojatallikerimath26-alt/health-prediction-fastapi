"""Input validation for patient records."""
import re
from datetime import date

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
NAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z .'-]{1,59}")
DATE_PATTERN = re.compile(r"(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4})")

# field: (label, minimum, maximum, unit)
RANGES = {
    "glucose": ("Glucose", 20, 600, "mg/dL"),
    "haemoglobin": ("Haemoglobin", 3, 25, "g/dL"),
    "cholesterol": ("Cholesterol", 50, 600, "mg/dL"),
}


def parse_dob(text):
    """Return (date, None) or (None, error message).

    Accepts dd/mm/yyyy and also dd.mm.yyyy or dd-mm-yyyy; the value is stored as dd/mm/yyyy.
    """
    match = DATE_PATTERN.fullmatch(text.strip())
    if not match:
        return None, "Date of birth must be in dd/mm/yyyy format."
    day, month, year = (int(part) for part in match.groups())
    try:
        dob = date(year, month, day)
    except ValueError:
        return None, f"{text.strip()} is not a real calendar date."
    if dob > date.today():
        return None, "Date of birth cannot be in the future."
    if year < 1900:
        return None, "Date of birth is too far in the past."
    return dob, None


def validate_patient(form):
    """Return (clean_values, list_of_error_messages)."""
    errors, clean = [], {}

    name = " ".join(form.get("full_name", "").split())
    if not NAME_PATTERN.fullmatch(name):
        errors.append("Full name must be 2-60 letters (spaces and . ' - are allowed).")
    clean["full_name"] = name

    dob, error = parse_dob(form.get("dob", ""))
    if error:
        errors.append(error)
    else:
        clean["dob"] = dob.strftime("%d/%m/%Y")

    raw_email = form.get("email", "").strip()
    if not EMAIL_PATTERN.fullmatch(raw_email):
        errors.append(f"'{raw_email}' is not a valid email address (expected name@domain.com).")
    clean["email"] = raw_email.lower()

    for field, (label, low, high, unit) in RANGES.items():
        raw = form.get(field, "").strip()
        try:
            value = float(raw)
        except ValueError:
            errors.append(f"{label} must be a number.")
            continue
        if not low <= value <= high:
            errors.append(f"{label} must be between {low} and {high} {unit}.")
        else:
            clean[field] = value

    return clean, errors
