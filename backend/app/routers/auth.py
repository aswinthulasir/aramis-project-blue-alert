from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import jwt
import bcrypt
import psycopg2
from datetime import datetime, timedelta

# Database connection
conn = psycopg2.connect(
    dbname="local",
    user="postgres",
    password="Aswin2000",
    host="localhost",
    port="5432",
)
cursor = conn.cursor()

# Secret key for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 2  # Token valid for 2 hours

# Define API Router
router = APIRouter()

# Request model
class AuthRequest(BaseModel):
    email: str
    password: str

# Function to generate JWT token
def create_jwt_token(user_id: str):
    expiration = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": user_id,
        "iat": datetime.utcnow(),
        "exp": expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Authentication route
@router.post("/auth/login")
def authenticate_user(request: AuthRequest):
    try:
        # Fetch user details from the database
        cursor.execute("SELECT u_id, email FROM users WHERE email = %s", (request.email,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        u_id = user[0]  # Extract user ID

        # Fetch hashed password from passwords table
        cursor.execute("SELECT password FROM passwords WHERE u_id = %s", (u_id,))
        stored_password = cursor.fetchone()

        if not stored_password:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Verify password
        if not bcrypt.checkpw(request.password.encode('utf-8'), stored_password[0].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Generate new JWT token
        access_token = create_jwt_token(u_id)

        # Store JWT token in the database
        cursor.execute("SELECT token FROM jwt_token WHERE user_id = %s", (u_id,))
        existing_token = cursor.fetchone()

        if existing_token:
            # Update existing token
            cursor.execute("UPDATE jwt_token SET token = %s WHERE user_id = %s", (access_token, u_id))
        else:
            # Insert new token
            cursor.execute("INSERT INTO jwt_token (user_id, token) VALUES (%s, %s)", (u_id, access_token))

        conn.commit()

        # Return the token and user ID for dashboard navigation
        return {
            "message": "Login successful",
            "user_id": u_id,
            "access_token": access_token
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
