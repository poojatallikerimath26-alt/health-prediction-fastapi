"""SQLite storage for patient records."""
import os
import sqlite3
from pathlib import Path

DB_PATH = os.getenv("HEALTH_DB", str(Path(__file__).parent / "health.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS patients (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name   TEXT NOT NULL,
    dob         TEXT NOT NULL,
    email       TEXT NOT NULL,
    glucose     REAL NOT NULL,
    haemoglobin REAL NOT NULL,
    cholesterol REAL NOT NULL,
    remarks     TEXT NOT NULL DEFAULT ''
)
"""


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        conn.execute(SCHEMA)


def list_patients():
    with connect() as conn:
        return conn.execute("SELECT * FROM patients ORDER BY id").fetchall()


def get_patient(patient_id):
    with connect() as conn:
        return conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()


def find_duplicate(values, exclude_id=None):
    """Same name + date of birth + email counts as the same patient."""
    with connect() as conn:
        row = conn.execute(
            "SELECT id FROM patients WHERE lower(full_name) = lower(?) AND dob = ? AND email = ? AND id != ?",
            (values["full_name"], values["dob"], values["email"], exclude_id or -1),
        ).fetchone()
    return row is not None


def create_patient(values):
    with connect() as conn:
        cursor = conn.execute(
            "INSERT INTO patients (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks) "
            "VALUES (:full_name, :dob, :email, :glucose, :haemoglobin, :cholesterol, :remarks)",
            values,
        )
        return cursor.lastrowid


def update_patient(patient_id, values):
    with connect() as conn:
        conn.execute(
            "UPDATE patients SET full_name = :full_name, dob = :dob, email = :email, glucose = :glucose, "
            "haemoglobin = :haemoglobin, cholesterol = :cholesterol, remarks = :remarks WHERE id = :id",
            {**values, "id": patient_id},
        )


def update_remarks(patient_id, remarks):
    with connect() as conn:
        conn.execute("UPDATE patients SET remarks = ? WHERE id = ?", (remarks, patient_id))


def delete_patient(patient_id):
    with connect() as conn:
        conn.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
