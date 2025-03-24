from fastapi import APIRouter, HTTPException
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

@router.get("/staffs/get")
def get_staffs():
    try:
        cursor.execute("SELECT s_name, role_id, activity FROM staffs")
        staffs = cursor.fetchall()

        if not staffs:
            raise HTTPException(status_code=404, detail="No staff records found")

        staff_list = []
        for staff in staffs:
            staff_list.append({
                "s_name": staff[0],
                "role_id": staff[1],
                "activity": staff[2]
            })

        return {"staffs": staff_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
