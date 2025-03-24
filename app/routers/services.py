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

# Pydantic model for service creation
class ServiceRequest(BaseModel):
    ser_name: str
    ser_desc: str
    ser_image: str  # Image URL
    ser_rate: float  # Service rate

@router.post("/services/post")
def create_service(service: ServiceRequest):
    try:
        # Insert into services table
        cursor.execute(
            "INSERT INTO services (ser_name, ser_desc, ser_image, ser_avl) VALUES (%s, %s, %s, %s) RETURNING ser_id",
            (service.ser_name, service.ser_desc, service.ser_image, True)  # Default availability is True
        )
        service_data = cursor.fetchone()
        conn.commit()

        if not service_data:
            raise HTTPException(status_code=500, detail="Failed to insert service")

        ser_id = service_data["ser_id"]

        # Insert into rates table
        cursor.execute(
            "INSERT INTO rates (ser_id, ser_rate) VALUES (%s, %s)",
            (ser_id, service.ser_rate)
        )
        conn.commit()

        return {"message": "Service added successfully", "ser_id": ser_id}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
