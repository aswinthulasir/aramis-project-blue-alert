from fastapi import APIRouter, HTTPException
import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="local",
    user="postgres",
    password="Aswin2000",
    host="localhost",
    port="5432",
)
cursor = conn.cursor()

# Define API Router
router = APIRouter()

@router.get("/patients/get")
def get_patients():
    try:
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()

        if not patients:
            raise HTTPException(status_code=404, detail="No patient records found")

        patients_list = []
        for patient in patients:
            patients_list.append({
                "p_id": patient[0],
                "p_name": patient[1],
                "p_dept": patient[2],
                "p_desc": patient[3],
                "p_age": patient[4],
                "p_doc": patient[5]
            })

        return {"patients": patients_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
