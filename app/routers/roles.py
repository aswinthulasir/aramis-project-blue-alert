from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2


conn = psycopg2.connect(
    dbname="local",
    user="postgres",
    password="Aswin2000",
    host="localhost",
    port="5432",
)
cursor = conn.cursor()


router = APIRouter()


class RoleRequest(BaseModel):
    role: str 

@router.post("/roles/add")
def add_role(role_data: RoleRequest):
    try:
        
        cursor.execute("INSERT INTO roles (role) VALUES (%s) RETURNING role_id", (role_data.role,))
        role_id = cursor.fetchone()[0]  
        conn.commit()

        return {
            "message": "Role added successfully",
            "role_id": role_id,
            "role": role_data.role
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
