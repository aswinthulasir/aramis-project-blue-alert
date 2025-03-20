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
class BillRequest(BaseModel):
    ser_id: int
    u_id: str
    p_id: int
    ser_rate: float
    payment_sts: bool

# POST route to add a bill
@router.post("/bills/post")
def add_bill(bill: BillRequest):
    try:
        # Insert into billing table
        cursor.execute(
            "INSERT INTO billing (ser_id, u_id, p_id, ser_rate, payment_sts) VALUES (%s, %s, %s, %s, %s) RETURNING bill_id",
            (bill.ser_id, bill.u_id, bill.p_id, bill.ser_rate, bill.payment_sts)
        )
        bill_data = cursor.fetchone()
        conn.commit()

        if not bill_data:
            raise HTTPException(status_code=500, detail="Failed to add bill")

        return {"message": "Bill added successfully", "bill_id": bill_data["bill_id"]}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
