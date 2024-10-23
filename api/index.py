from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.allocation import create_allocation, update_allocation, delete_allocation, get_allocation_history
from .skeleton import AllocationCreate, AllocationUpdate, AllocationHistory

app = FastAPI()

@app.post("/allocations/create")
async def allocate_vehicle(request: AllocationCreate):
    result = await create_allocation(request.employee_id, request.vehicle_id, request.allocation_date)
    return result

@app.post("/allocations/update/{allocation_id}")
async def modify_allocation(allocation_id: str, request: AllocationUpdate):
    result = await update_allocation(allocation_id, request.employee_id, request.vehicle_id, request.allocation_date)
    return result

@app.post("/allocations/delete/{allocation_id}")
async def remove_allocation(allocation_id: str):
    result = await delete_allocation(allocation_id)
    return result

@app.post("/allocations/history")
async def fetch_allocation_history(request: AllocationHistory):
    result = await get_allocation_history(request.employee_id, request.allocation_date)
    return result

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "status_code": 404,
            "success_message": None,
            "error_message": "Endpoint not found.",
        }
    )

@app.exception_handler(405)
async def method_not_allowed_handler(request, exc):
    return JSONResponse(
        status_code=405,
        content={
            "status_code": 405,
            "success_message": None,
            "error_message": "Method not allowed",
        }
    )
