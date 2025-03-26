from fastapi import APIRouter, HTTPException
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

@router.get("/services/get")
def get_services():
    try:
        # Fetch services with their rates from the 'rates' table
        cursor.execute("""
            SELECT s.ser_id, s.ser_name, s.ser_desc, s.ser_image, s.ser_avl, r.ser_rate
            FROM services s
            LEFT JOIN rates r ON s.ser_id = r.ser_id
        """)
        services = cursor.fetchall()

        if not services:
            raise HTTPException(status_code=404, detail="No service found")

        services_list = []
        for service in services:
            services_list.append({
                "ser_id": service[0],
                "ser_name": service[1],
                "ser_desc": service[2],
                "ser_image": service[3],
                "ser_avl": service[4],
                "ser_rate": float(service[5]) if service[5] is not None else 0  # Ensure a numeric value
            })

        return {"services": services_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rates/get/{ser_id}")
def get_service_rate(ser_id: int):
    try:
        cursor.execute("SELECT ser_rate FROM rates WHERE ser_id = %s", (ser_id,))
        rate = cursor.fetchone()

        if rate is None:
            raise HTTPException(status_code=404, detail="Rate not found for given service ID")

        return {"ser_id": ser_id, "ser_rate": float(rate[0])}  # Convert Decimal to float

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

