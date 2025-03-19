from fastapi import FastAPI
import psycopg2
from app.config import settings

app = FastAPI() 

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

try:
    conn = psycopg2.connect(
        host=settings.database_hostname,
        port=settings.database_port,
        dbname=settings.database_name,
        user=settings.database_username,
        password=settings.database_password
    )
    print("Database connected successfully!")
    print(settings.database_hostname)
    print(settings.database_port)
    print(settings.database_name)
    conn.close()
except Exception as e:
    print(f"Database connection failed: {e}")