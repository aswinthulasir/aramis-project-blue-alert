from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
import jwt
import os
import random
import string
from typing import Optional
from app.routers.services import router as services_router
from app.routers.patients import router as patients_router
from app.routers.bills import router as bills_router

app = FastAPI()

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

# JWT Secret Key
# SECRET_KEY = "your_secret_key"

class RegisterRequest(BaseModel):
    email: str
    password: str
    username: Optional[str] = None 
    role_id: int
    s_name: str
    
app.include_router(services_router)
app.include_router(patients_router)
app.include_router(bills_router)


@app.post("/users/register")
def register_user(user: RegisterRequest):
    try:
        # Step 1: Insert into users table and get u_id
        cursor.execute(
            "INSERT INTO users (email) VALUES (%s) RETURNING u_id, staff_id",
            (user.email,)
        )
        user_data = cursor.fetchone()
        conn.commit()
        
        if not user_data:
            raise HTTPException(status_code=500, detail="Failed to register user")

        u_id = user_data["u_id"]
        staff_id = user_data["staff_id"]

        # Step 2: Hash the password and insert into passwords table
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cursor.execute(
            "INSERT INTO passwords (u_id, password) VALUES (%s, %s)",
            (u_id, hashed_password)
        )
        
        # Step 3: Insert into staffs table
        cursor.execute(
            "INSERT INTO staffs (staff_id, u_id, s_name , role_id, activity) VALUES (%s,%s, %s, %s, %s)",
            (staff_id, u_id, user.s_name, user.role_id, True)  
        )

        # Step 4: Generate JWT Token and store it in auth table
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        cursor.execute(
            "INSERT INTO auth (u_id, jwt_token) VALUES (%s, %s)",
            (u_id, token)
        )

        conn.commit()

        return {"message": "User registered successfully", "u_id": u_id, "token": token}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
