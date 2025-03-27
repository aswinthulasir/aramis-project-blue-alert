from fastapi import APIRouter
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

@router.get("/bills/today")
def get_today_bills():
    try:
        cur = conn.cursor()
        today = date.today()  # Get today's date
        
        query = "SELECT * FROM billing WHERE DATE(bill_date) = %s"
        cur.execute(query, (today,))
        bills = cur.fetchall()
        cur.close()

        return {"bills": bills}

    except Exception as e:
        return {"error": str(e)}
