from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="local",
    user="postgres",
    password="Aswin2000",
    host="localhost",
    port="5432",
)
cursor = conn.cursor()

# Define API Router
router = APIRouter()

# Request model for adding a role
class RoleRequest(BaseModel):
    role: str  # Role name

@router.post("/roles/add")
def add_role(role_data: RoleRequest):
    try:
        # Insert new role into the database
        cursor.execute("INSERT INTO roles (role) VALUES (%s) RETURNING role_id", (role_data.role,))
        role_id = cursor.fetchone()[0]  # Fetch the generated role_id
        conn.commit()

        return {
            "message": "Role added successfully",
            "role_id": role_id,
            "role": role_data.role
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
