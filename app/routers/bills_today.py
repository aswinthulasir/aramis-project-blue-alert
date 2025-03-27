from fastapi import APIRouter, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import date

router = APIRouter()

# Database Connection
conn = psycopg2.connect(
    dbname="local",
    user="postgres",
    password="Aswin2000",
    host="localhost",
    port="5432",
    cursor_factory=RealDictCursor
)
cursor = conn.cursor()

@router.get("/bills/today")
def get_todays_bills():
    today = date.today()

    # Fetch today's bills
    cursor.execute("SELECT * FROM billing WHERE DATE(bill_date) = %s", (today,))
    bills = cursor.fetchall()

    # Fetch total collected amount for today (paid bills)
    cursor.execute("""
        SELECT COALESCE(SUM(ser_rate), 0) AS total_collected 
        FROM billing 
        WHERE DATE(bill_date) = %s AND payment_sts = TRUE
    """, (today,))
    total_collected = cursor.fetchone()["total_collected"]

    # Fetch pending payments for today
    cursor.execute("""
        SELECT * FROM billing 
        WHERE DATE(bill_date) = %s AND payment_sts = FALSE
    """, (today,))
    pending_bills = cursor.fetchall()

    # Calculate total pending amount
    cursor.execute("""
        SELECT COALESCE(SUM(ser_rate), 0) AS total_pending 
        FROM billing 
        WHERE DATE(bill_date) = %s AND payment_sts = FALSE
    """, (today,))
    total_pending = cursor.fetchone()["total_pending"]

    return {
        "bills": bills,
        "total_collected": total_collected,
        "pending_bills": pending_bills,
        "total_pending": total_pending
    }
