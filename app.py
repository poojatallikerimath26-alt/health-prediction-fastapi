"""Health Prediction App - FastAPI backend with server-rendered pages."""
from pathlib import Path
from urllib.parse import urlencode

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import config

config.load_env()

import ai_client  # noqa: E402  (imported after .env is loaded)
import database as db  # noqa: E402
import validators  # noqa: E402

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
FIELDS = ("full_name", "dob", "email", "glucose", "haemoglobin", "cholesterol")

db.init_db()
app = FastAPI(title="Health Prediction App")


def render(request, template, status_code=200, **context):
    return templates.TemplateResponse(request, template, context, status_code=status_code)


def back_home(message):
    return RedirectResponse("/?" + urlencode({"msg": message}), status_code=303)


def make_remarks(values):
    """Ask the AI for a prediction; store a clear note if it cannot answer."""
    try:
        return ai_client.get_remarks(values)
    except ai_client.AIError as error:
        return f"{ai_client.UNAVAILABLE} ({error}). Use Regenerate to retry."


def require_patient(patient_id):
    patient = db.get_patient(patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return patient


@app.get("/")
def home(request: Request, msg: str = ""):
    return render(request, "index.html", patients=db.list_patients(), form={}, errors=[], msg=msg)


@app.post("/patients")
def create(
    request: Request,
    full_name: str = Form(""), dob: str = Form(""), email: str = Form(""),
    glucose: str = Form(""), haemoglobin: str = Form(""), cholesterol: str = Form(""),
):
    form = dict(full_name=full_name, dob=dob, email=email,
                glucose=glucose, haemoglobin=haemoglobin, cholesterol=cholesterol)
    values, errors = validators.validate_patient(form)
    if not errors and db.find_duplicate(values):
        errors.append("Duplicate record: a patient with the same name, date of birth and email already exists.")
    if errors:
        return render(request, "index.html", 400, patients=db.list_patients(), form=form, errors=errors, msg="")

    values["remarks"] = make_remarks(values)
    db.create_patient(values)
    return back_home(f"Saved {values['full_name']}.")


@app.get("/patients/{patient_id}/edit")
def edit_form(request: Request, patient_id: int):
    patient = require_patient(patient_id)
    return render(request, "edit.html", patient=patient, form=dict(patient), errors=[])


@app.post("/patients/{patient_id}/edit")
def update(
    request: Request, patient_id: int,
    full_name: str = Form(""), dob: str = Form(""), email: str = Form(""),
    glucose: str = Form(""), haemoglobin: str = Form(""), cholesterol: str = Form(""),
):
    patient = require_patient(patient_id)
    form = dict(full_name=full_name, dob=dob, email=email,
                glucose=glucose, haemoglobin=haemoglobin, cholesterol=cholesterol)
    values, errors = validators.validate_patient(form)
    if not errors and db.find_duplicate(values, exclude_id=patient_id):
        errors.append("Duplicate record: another patient already has the same name, date of birth and email.")
    if errors:
        return render(request, "edit.html", 400, patient=patient, form=form, errors=errors)

    inputs_changed = any(values[k] != patient[k] for k in ("dob", "glucose", "haemoglobin", "cholesterol"))
    still_unavailable = patient["remarks"].startswith(ai_client.UNAVAILABLE)
    values["remarks"] = make_remarks(values) if inputs_changed or still_unavailable else patient["remarks"]
    db.update_patient(patient_id, values)
    return back_home(f"Updated {values['full_name']}.")


@app.post("/patients/{patient_id}/delete")
def delete(patient_id: int):
    patient = require_patient(patient_id)
    db.delete_patient(patient_id)
    return back_home(f"Deleted {patient['full_name']}.")


@app.post("/patients/{patient_id}/regenerate")
def regenerate(patient_id: int):
    patient = require_patient(patient_id)
    remarks = make_remarks(dict(patient))
    db.update_remarks(patient_id, remarks)
    return back_home(f"Remarks refreshed for {patient['full_name']}.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000)
