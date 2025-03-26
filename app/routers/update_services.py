from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2

# Database Connection
conn = psycopg2.connect(
    dbname="local",
    user="postgres",
    password="Aswin2000",
    host="localhost",
    port="5432",
)
cursor = conn.cursor()

router = APIRouter()

# Request Body Models
class UpdateServiceName(BaseModel):
    ser_name: str

class UpdateServiceDesc(BaseModel):
    ser_desc: str

class UpdateServiceImage(BaseModel):
    ser_image: str

class UpdateServiceAvailability(BaseModel):
    ser_avl: bool

# Update Service Name
@router.put("/services/update-name/{ser_id}")
def update_service_name(ser_id: int, request: UpdateServiceName):
    try:
        cursor.execute("UPDATE services SET ser_name = %s WHERE ser_id = %s", (request.ser_name, ser_id))
        conn.commit()
        return {"message": "Service name updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Update Service Description
@router.put("/services/update-desc/{ser_id}")
def update_service_desc(ser_id: int, request: UpdateServiceDesc):
    try:
        cursor.execute("UPDATE services SET ser_desc = %s WHERE ser_id = %s", (request.ser_desc, ser_id))
        conn.commit()
        return {"message": "Service description updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Update Service Image
@router.put("/services/update-image/{ser_id}")
def update_service_image(ser_id: int, request: UpdateServiceImage):
    try:
        cursor.execute("UPDATE services SET ser_image = %s WHERE ser_id = %s", (request.ser_image, ser_id))
        conn.commit()
        return {"message": "Service image updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Update Service Availability
@router.put("/services/update-availability/{ser_id}")
def update_service_availability(ser_id: int, request: UpdateServiceAvailability):
    try:
        cursor.execute("UPDATE services SET ser_avl = %s WHERE ser_id = %s", (request.ser_avl, ser_id))
        conn.commit()
        return {"message": "Service availability updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))