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
router = APIRouter()

@router.get("/staffs/get")
def get_staffs():
    try:
        with conn.cursor() as cursor:  # Use a new cursor inside the function
            cursor.execute("SELECT staff_id, s_name, role_id, activity FROM staffs")
            staffs = cursor.fetchall()

            if not staffs:
                raise HTTPException(status_code=404, detail="No staff records found")

            staff_list = []
            for staff in staffs:
                staff_list.append({
                    "staff_id": staff[0],
                    "s_name": staff[1],
                    "role_id": staff[2],
                    "activity": staff[3]
                })

            return {"staffs": staff_list}

    except psycopg2.Error as e:
        conn.rollback()  # Rollback transaction to avoid aborted state
        raise HTTPException(status_code=500, detail=str(e))
