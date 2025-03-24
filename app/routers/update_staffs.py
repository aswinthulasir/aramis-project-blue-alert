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

# Request Body Model
class StaffNameUpdate(BaseModel):
    s_name: str

# Update Staff Name
@router.put("/staffs/update-name/{staff_id}")
def update_staff_name(staff_id: int, request: StaffNameUpdate):
    try:
        cursor.execute("UPDATE staffs SET s_name = %s WHERE staff_id = %s", (request.s_name, staff_id))
        conn.commit()
        return {"message": "Staff name updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))





class StaffActivityUpdate(BaseModel):
    activity: bool  # Boolean field for activity status (True/False)

# Update Staff Activity
@router.put("/staffs/update-activity/{staff_id}")
def update_staff_activity(staff_id: int, request: StaffActivityUpdate):
    try:
        cursor.execute("UPDATE staffs SET activity = %s WHERE staff_id = %s", (request.activity, staff_id))
        conn.commit()
        return {"message": "Staff activity updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))




class StaffRoleUpdate(BaseModel):
    role_id: int  # Role ID should be an integer

# Update Staff Role
@router.put("/staffs/update-role/{staff_id}")
def update_staff_role(staff_id: int, request: StaffRoleUpdate):
    try:
        cursor.execute("UPDATE staffs SET role_id = %s WHERE staff_id = %s", (request.role_id, staff_id))
        conn.commit()
        return {"message": "Staff role updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
