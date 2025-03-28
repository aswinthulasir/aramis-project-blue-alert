from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
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

# Pydantic Model for Bill Request
class BillRequest(BaseModel):
    ser_id: int
    staff_id: int
    p_id: int
    payment_sts: bool
    bill_cfm: bool


@router.post("/bills/post")
def add_bill(bill: BillRequest):
    try:
        
        cursor.execute("SELECT ser_rate FROM rates WHERE ser_id = %s", (bill.ser_id,))
        service_data = cursor.fetchone()

        
        print("Fetched service rate:", service_data) 

        if not service_data:
            raise HTTPException(status_code=400, detail="Invalid service ID or rate not found.")

        ser_rate = float(service_data["ser_rate"])  # Explicitly convert to float

        
        cursor.execute(
            "INSERT INTO billing (ser_id, staff_id, p_id, ser_rate, payment_sts, bill_cfm) VALUES (%s, %s, %s, %s, %s, %s) RETURNING bill_id",
            (bill.ser_id, bill.staff_id, bill.p_id, ser_rate, bill.payment_sts, bill.bill_cfm)
        )
        bill_data = cursor.fetchone()
        conn.commit()

        return {"message": "Bill added successfully", "bill_id": bill_data["bill_id"]}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

