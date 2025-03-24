from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import asyncpg
import bcrypt
import jwt
import os
import random
import string
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware




# Routers
from app.routers.services import router as services_router
from app.routers.patients import router as patients_router
from app.routers.bills import router as bills_router
from app.routers.auth import router as auth_router
from app.routers.fetch_users import router as fetch_users_router
from app.routers.fetch_services import router as fetch_services_router
from app.routers.roles import router as roles_router
from app.routers.fetch_roles import router as fetch_roles_router
from app.routers.fetch_billing import router as fetch_billing_router
from app.routers.fetch_patients import router as fetch_patients_router
from app.routers.update_staffs import router as update_staffs_router
from app.routers.update_services import router as update_services_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Database Connection
DATABASE_URL = "postgresql://postgres:Aswin2000@localhost:5432/local"

async def connect_db():
    return await asyncpg.create_pool(DATABASE_URL)

db_pool = None  # Global variable for the database pool

@app.on_event("startup")
async def startup():
    global db_pool
    db_pool = await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await db_pool.close()

# Dependency to get database connection
async def get_db():
    async with db_pool.acquire() as connection:
        yield connection

# JWT Secret Key
SECRET_KEY = "your_secret_key"

class RegisterRequest(BaseModel):
    email: str
    password: str
    username: Optional[str] = None 
    role_id: int
    s_name: str

# Register Routers
app.include_router(services_router)
app.include_router(patients_router)
app.include_router(bills_router)
app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(fetch_users_router)
app.include_router(fetch_services_router)
app.include_router(fetch_roles_router)
app.include_router(fetch_billing_router)
app.include_router(fetch_patients_router)
app.include_router(update_staffs_router)
app.include_router(update_services_router)

# User Registration Route
@app.post("/users/register")
async def register_user(user: RegisterRequest, db=Depends(get_db)):
    try:
        # Step 1: Insert into users table and get u_id
        user_data = await db.fetchrow(
            "INSERT INTO users (email) VALUES ($1) RETURNING u_id, staff_id",
            user.email
        )

        if not user_data:
            raise HTTPException(status_code=500, detail="Failed to register user")

        u_id = user_data["u_id"]
        staff_id = user_data["staff_id"]

        # Step 2: Hash the password and insert into passwords table
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        await db.execute(
            "INSERT INTO passwords (u_id, password) VALUES ($1, $2)",
            u_id, hashed_password
        )
        
        # Step 3: Insert into staffs table
        await db.execute(
            "INSERT INTO staffs (staff_id, u_id, s_name , role_id, activity) VALUES ($1, $2, $3, $4, $5)",
            staff_id, u_id, user.s_name, user.role_id, True  
        )

        # Step 4: Generate JWT Token and store it in auth table
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        await db.execute(
            "INSERT INTO auth (u_id, jwt_token) VALUES ($1, $2)",
            u_id, token
        )

        return {"message": "User registered successfully", "u_id": u_id, "token": token}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
