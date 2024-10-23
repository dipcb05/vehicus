import pytest
from fastapi.testclient import TestClient
from api.index import app  

client = TestClient(app)

def test_create_allocation():
    response = client.post("/allocations", params={
        "employee_id": "dip",
        "vehicle_id": "vehicle123",
        "allocation_date": "2024-10-25"
    })
    assert response.status_code == 201
    assert response.json()["success_message"] == "success"
    print(f"Create Allocation details - {response.json()}")

def test_update_allocation():
    response = client.post("/allocations", params={
        "employee_id": "dip1234",
        "vehicle_id": "vehicle456",
        "allocation_date": "2024-10-25"
    })
    allocation_id = response.json().get("vehicle_id") 
    response = client.post(f"/allocations/update/{allocation_id}", params={
        "employee_id": "dip1234",
        "vehicle_id": "vehicle789",
        "allocation_date": "2024-10-26"
    })
    assert response.status_code == 200
    assert response.json()["success_message"] == "success"
    print(f"Update Allocation details - {response.json()}")

def test_delete_allocation():

    response = client.post("/allocations", params={
        "employee_id": "dip_delete",
        "vehicle_id": "vehicle098",
        "allocation_date": "2024-10-25"
    })
    allocation_id = response.json().get("vehicle_id")
    response = client.post(f"/allocations/delete/{allocation_id}")
    assert response.status_code == 200
    assert response.json()["success_message"] == "success"
    print(f"Delete Allocation details - {response.json()}")

def test_get_allocation_history():

    test_create_allocation()

    response = client.post("/allocations/history", params={
        "employee_id": "dip"
    })
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0
    print(f"Get Allocation details - {response.json()}")
