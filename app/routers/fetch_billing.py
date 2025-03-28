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

@router.get("/billing/get")
def get_billing():
    try:
        cursor.execute("SELECT * FROM billing")
        billings = cursor.fetchall()

        if not billings:
            raise HTTPException(status_code=404, detail="No billing records found")

        billing_list = []
        for billing in billings:
            billing_list.append({
                "bill_id": billing[0],
                "ser_id": billing[1],
                "u_id": billing[2],
                "p_id": billing[3],
                "ser_rate": float(billing[4]), 
                "payment_sts": billing[5]  
            })

        return {"billing": billing_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
