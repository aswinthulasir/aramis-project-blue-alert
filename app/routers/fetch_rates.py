from fastapi import APIRouter, HTTPException
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

@router.get("/rates/get/{ser_id}")
def get_service_rate(ser_id: int):
    try:
        cursor.execute("SELECT ser_rate FROM rates WHERE ser_id = %s", (ser_id,))
        rate_data = cursor.fetchone()
        
        if not rate_data:
            raise HTTPException(status_code=404, detail="Service rate not found")

        return {"ser_id": ser_id, "ser_rate": rate_data["ser_rate"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
