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
        cursor.execute("SELECT ser_id, ser_name, ser_desc, ser_image, ser_avl FROM services")
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
                "ser_avl": service[4]
            })

        return {"services": services_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
