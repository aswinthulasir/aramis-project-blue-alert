from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict

router = APIRouter()

# Database Connection Dependency
def get_db():
    try:
        conn = psycopg2.connect(
            dbname="local",
            user="postgres",
            password="Aswin2000",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        yield cursor, conn  # Yield cursor and connection for transactions
    finally:
        cursor.close()
        conn.close()

# Pydantic Model for Bill Request
class BillRequest(BaseModel):
    ser_id: int
    staff_id: int
    p_id: int
    payment_sts: bool
    bill_cfm: bool

# POST Route to Add a Bill
@router.post("/bills/post")
def add_bill(bill: BillRequest, db: tuple = Depends(get_db)) -> Dict:
    cursor, conn = db  # Unpack database connection
    try:
        # Fetch service rate from rates table
        cursor.execute("SELECT ser_rate FROM rates WHERE ser_id = %s", (bill.ser_id,))
        service_data = cursor.fetchone()

        # Debugging: Print fetched service rate
        print("Fetched service rate:", service_data)

        if not service_data:
            raise HTTPException(status_code=400, detail="Invalid service ID or rate not found.")

        ser_rate = float(service_data["ser_rate"])  # Explicitly convert to float

        # Insert into billing table
        cursor.execute(
            """INSERT INTO billing (ser_id, staff_id, p_id, ser_rate, payment_sts, bill_cfm)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING bill_id""",
            (bill.ser_id, bill.staff_id, bill.p_id, ser_rate, bill.payment_sts, bill.bill_cfm)
        )
        bill_data = cursor.fetchone()
        conn.commit()

        return {"message": "Bill added successfully", "bill_id": bill_data["bill_id"]}

    except Exception as e:
        conn.rollback()
        print("Error inserting bill:", str(e))  # Print for debugging
        raise HTTPException(status_code=500, detail="Database insertion failed.")
