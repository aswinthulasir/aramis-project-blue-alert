import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.main import app 


import pytest
from httpx import AsyncClient
from main import app  



@pytest.mark.asyncio
async def test_get_services():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/services/get")
        assert response.status_code == 200
        assert "services" in response.json()

@pytest.mark.asyncio
async def test_get_service_rate():
    service_id = 1  # Replace with a valid service ID from your DB
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/rates/get/{service_id}")
        assert response.status_code == 200
        assert "ser_rate" in response.json()

@pytest.mark.asyncio
async def test_get_patients():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/patients/get")
        assert response.status_code == 200
        assert "patients" in response.json()

@pytest.mark.asyncio
async def test_add_bill():
    bill_data = {
        "ser_id": 1,  # Replace with valid IDs
        "staff_id": 101,
        "p_id": 1,
        "ser_rate": 500.00,
        "payment_sts": True,
        "bill_cfm": True
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/bills/post", json=bill_data)
        assert response.status_code == 201  # Ensure successful creation
        assert response.json()["message"] == "Bill added successfully!"
