from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor

router = APIRouter()


conn = psycopg2.connect(
    dbname="local",
    user="postgres",
    password="Aswin2000",
    host="localhost",
    port="5432",
    cursor_factory=RealDictCursor
)
cursor = conn.cursor()

# GET Route to Fetch Individual Bills of a Patient
@router.get("/bills/{p_id}")
def get_patient_bills(p_id: int):
    try:
        cursor.execute("SELECT * FROM billing WHERE p_id = %s", (p_id,))
        bills = cursor.fetchall()

        if not bills:
            return []

        # Convert bill_date to a string format
        for bill in bills:
            bill["bill_date"] = bill["bill_date"].isoformat()  # Converts datetime to string

        return bills

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
