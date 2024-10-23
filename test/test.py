import pytest
from fastapi.testclient import TestClient
from api.index import app  

client = TestClient(app)

# Testing app creation is working
def test_create_allocation():
    response = client.post("/allocations/create", json={
        "employee_id": "dip",
        "vehicle_id": "67182c70d3047dab854b6564",
        "allocation_date": "2024-10-25"
    })
    assert response.status_code == 200
    print(f"Create Allocation details - {response.json()}")

# Testing update allocation is working
def test_update_allocation():
    
    # Create an allocation
    response = client.post("/allocations/create", json={
        "employee_id": "dip1234",
        "vehicle_id": "67182c70d3047dab854b6568",
        "allocation_date": "2024-10-25"
    })

    # Update the same allocation by extracting allocation_id

    allocation_id = response.json().get("allocation_id") 

    response = client.post(f"/allocations/update/{allocation_id}", json={
        "employee_id": "dip1234",
        "vehicle_id": "67182c70d3047dab854b6578",
        "allocation_date": "2024-10-26"
    })
    assert response.status_code == 200
    print(f"Update Allocation details - {response.json()}")

# Testing delete allocation is working
def test_delete_allocation():
    
    # Create an allocation
    response = client.post("/allocations/create", json={
        "employee_id": "dip_delete",
        "vehicle_id": "67182c70d3047dab854b6569",
        "allocation_date": "2024-10-25"
    })
    allocation_id = response.json().get("allocation_id")

    # Delete the same allocation
    response = client.post(f"/allocations/delete/{allocation_id}")
    assert response.status_code == 200
    print(f"Delete Allocation details - {response.json()}")

# Testing allocation read is working
def test_get_allocation_history():

    # Create an allocation first
    test_create_allocation()

    # Fetch same allocation
    response = client.post("/allocations/history", json={
        "employee_id": "dip"
    })
    assert response.status_code == 200
    print(f"Get Allocation details - {response.json()}")
