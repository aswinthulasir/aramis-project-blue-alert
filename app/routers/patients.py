from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

router = APIRouter()

# Database connection
conn = psycopg2.connect(
    dbname="local",
    user="postgres",
    password="Aswin2000",
    host="localhost",
    port="5432",
    cursor_factory=RealDictCursor
)
cursor = conn.cursor()

# Pydantic Model
class PatientRequest(BaseModel):
    p_name: str
    p_dept: str
    p_desc: str
    p_age: int
    p_doc: str

# POST route to add a patient
@router.post("/patients/post")
def add_patient(patient: PatientRequest):
    try:
        # Insert into patients table
        cursor.execute(
            "INSERT INTO patients (p_name, p_dept, p_desc, p_age, p_doc) VALUES (%s, %s, %s, %s, %s) RETURNING p_id",
            (patient.p_name, patient.p_dept, patient.p_desc, patient.p_age, patient.p_doc)
        )
        patient_data = cursor.fetchone()
        conn.commit()

        if not patient_data:
            raise HTTPException(status_code=500, detail="Failed to add patient")

        return {"message": "Patient added successfully", "p_id": patient_data["p_id"]}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
