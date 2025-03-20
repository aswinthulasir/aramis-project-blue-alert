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

@router.get("/roles/get")
def get_roles():
    try:
        cursor.execute("SELECT * FROM roles")
        roles = cursor.fetchall()

        if not roles:
            raise HTTPException(status_code=404, detail="No roles found")

        roles_list = []
        for role in roles:
            roles_list.append({
                "role_id": role[0],
                "role": role[1]
            })

        return {"roles": roles_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
