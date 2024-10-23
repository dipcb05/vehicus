from config.db import db
from config.redis import redis_client
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from bson import ObjectId
from bson.objectid import ObjectId
import time
import os
import json

CACHE_TIMEOUT = os.getenv("CACHE_TIMEOUT", 600)


async def create_allocation(employee_id: str, vehicle_id: str, allocation_date: str):
    start_time = time.time()
    try:
        allocation_date_obj = datetime.strptime(allocation_date, '%Y-%m-%d') 
        current_date_obj = datetime.now().date()


        allocation_data = await redis_client.get(f"allocation:{employee_id}")
        
        if allocation_data:
            return {
                "status_code": 400,
                "success_message": None,
                "error_message": "Vehicle is already allocated",
                "vehicle_id": vehicle_id,
                "employee_id": None,
                "driver_id": None,
                "response_time": round(time.time() - start_time, 3)
            }

        existing_allocation = await db.allocations.find_one({
            "vehicle_id": vehicle_id,
            "allocation_date": allocation_date_obj
        })

        if existing_allocation:
            return {
                "status_code": 400,
                "success_message": None,
                "error_message": "Vehicle is already allocated",
                "vehicle_id": vehicle_id,
                "employee_id": None,
                "driver_id": None,
                "response_time": round(time.time() - start_time, 3)
            }

        vehicle = await db.vehicles.find_one({"_id": ObjectId(vehicle_id)}, {"driver_id": 1})

        if not vehicle:
            return {
                "status_code": 400,
                "success_message": None,
                "error_message": "Vehicle not found",
                "vehicle_id": None,
                "employee_id": None,
                "driver_id": None,
                "response_time": round(time.time() - start_time, 3)
            }
        
        if allocation_date_obj.date() < current_date_obj:
            return {
                "status_code": 400,
                "success_message": None,
                "error_message": "Invalid date",
                "vehicle_id": None,
                "employee_id": None,
                "driver_id": None,
                "response_time": round(time.time() - start_time, 3)
            }
            
        driver_id = vehicle["driver_id"]

        allocation = {
            "employee_id": employee_id,
            "vehicle_id": vehicle_id,
            "driver_id": driver_id,
            "allocation_date": allocation_date_obj
        }
        result = await db.allocations.insert_one(allocation)
        inserted_id = result.inserted_id
        await redis_client.set(f"allocation:{employee_id}:{vehicle_id}", json.dumps(allocation, default=str))

        return {
            "status_code": 201,
            "success_message": "success",
            "error_message": None,
            "allocation_id": str(inserted_id),
            "vehicle_id": vehicle_id,
            "employee_id": employee_id,
            "driver_id": driver_id,
            "response_time": round(time.time() - start_time, 3)
        }
    except Exception as e:
        return {
            "status_code": 500,
            "success_message": None,
            "error_message": str(e),
            "vehicle_id": None,
            "employee_id": None,
            "driver_id": None,
            "response_time": round(time.time() - start_time, 3)
        }

async def update_allocation(allocation_id: str, employee_id: str, vehicle_id: str, allocation_date: str):
    start_time = time.time()
    try:
        allocation_date_obj = datetime.strptime(allocation_date, '%Y-%m-%d')
        current_date_obj = datetime.now().date()

        allocation = await db.allocations.find_one({"_id": ObjectId(allocation_id)})

        if not allocation:
            return {
                "status_code": 404,
                "success_message": None,
                "error_message": "Allocation not found",
                "vehicle_id": None,
                "employee_id": None,
                "driver_id": None,
                "response_time": round(time.time() - start_time, 3)
            }

        if allocation_date_obj.date() < current_date_obj:
            return {
                "status_code": 400,
                "success_message": None,
                "error_message": "Invalid date",
                "vehicle_id": None,
                "employee_id": None,
                "driver_id": None,
                "response_time": round(time.time() - start_time, 3)
            }

        existing_allocation = await db.allocations.find_one({
            "vehicle_id": vehicle_id,
            "allocation_date": allocation_date_obj
        })

        if existing_allocation and existing_allocation["_id"] != allocation["_id"]:
            return {
                "status_code": 400,
                "success_message": None,
                "error_message": "Vehicle is already allocated",
                "vehicle_id": vehicle_id,
                "employee_id": None,
                "driver_id": None,
                "response_time": round(time.time() - start_time, 3)
            }

        update_result = await db.allocations.update_one(
            {"_id": ObjectId(allocation_id)},
            {"$set": {
                "employee_id": employee_id,
                "vehicle_id": vehicle_id,
                "allocation_date": allocation_date_obj
            }}
        )

        if update_result.modified_count:
            allocation_data = {
                "employee_id": employee_id,
                "vehicle_id": vehicle_id,
                "allocation_date": allocation_date,
                "driver_id": allocation["driver_id"]
            }
            await redis_client.set(f"allocation:{allocation_id}", json.dumps(allocation_data, default=str))

            return {
                "status_code": 200,
                "success_message": "Success",
                "error_message": None,
                "vehicle_id": vehicle_id,
                "employee_id": employee_id,
                "driver_id": allocation["driver_id"],
                "allocation_date": allocation_date,
                "response_time": round(time.time() - start_time, 3)
            }

        return {
            "status_code": 400,
            "success_message": None,
            "error_message": "No Changes",
            "vehicle_id": None,
            "employee_id": None,
            "driver_id": None,
            "response_time": round(time.time() - start_time, 3)
        }

    except Exception as e:
        return {
            "status_code": 500,
            "success_message": None,
            "error_message": str(e),
            "vehicle_id": None,
            "employee_id": None,
            "driver_id": None,
            "response_time": round(time.time() - start_time, 3)
        }

from datetime import datetime
from bson import ObjectId

async def delete_allocation(allocation_id: str):
    start_time = time.time()
    try:
        allocation = await db.allocations.find_one({"_id": ObjectId(allocation_id)})
        if not allocation:
            return {
                "status_code": 404,
                "success_message": None,
                "error_message": "Allocation not found",
                "vehicle_id": None,
                "employee_id": None,
                "driver_id": None,
                "response_time": round(time.time() - start_time, 3)
            }
        allocation_date = allocation["allocation_date"]
        if isinstance(allocation_date, str):
            allocation_date_obj = datetime.strptime(allocation_date, '%Y-%m-%d').date()
        elif isinstance(allocation_date, datetime):
            allocation_date_obj = allocation_date.date()
        else:
            return {
                "status_code": 400,
                "success_message": None,
                "error_message": "Invalid allocation_date format",
                "vehicle_id": None,
                "employee_id": None,
                "driver_id": None,
                "response_time": round(time.time() - start_time, 3)
            }
        if allocation_date_obj < datetime.now().date():
            return {
                "status_code": 400,
                "success_message": None,
                "error_message": "Time expired",
                "vehicle_id": None,
                "employee_id": None,
                "driver_id": None,
                "response_time": round(time.time() - start_time, 3)
            }
        delete_result = await db.allocations.delete_one({"_id": ObjectId(allocation_id)})

        if delete_result.deleted_count:
            await redis_client.delete(allocation_id)
            return {
                "status_code": 200,
                "success_message": "success",
                "error_message": None,
                "vehicle_id": allocation["vehicle_id"],
                "employee_id": allocation["employee_id"],
                "driver_id": allocation["driver_id"],
                "allocation_date": allocation["allocation_date"],
                "response_time": round(time.time() - start_time, 3)
            }

        return {
            "status_code": 400,
            "success_message": None,
            "error_message": "Something went wrong",
            "vehicle_id": None,
            "employee_id": None,
            "driver_id": None,
            "response_time": round(time.time() - start_time, 3)
        }

    except Exception as e:
        return {
            "status_code": 500,
            "success_message": None,
            "error_message": str(e),
            "vehicle_id": None,
            "employee_id": None,
            "driver_id": None,
            "response_time": round(time.time() - start_time, 3)
        }

async def get_allocation_history(employee_id: str = None, allocation_date: str = None):
    start_time = time.time()
    try:
        allocation_data = await redis_client.get(f"allocation:{employee_id}")
        
        if allocation_data:
            return {
                "status_code": 200,
                "success_message": "success",
                "error_message": None,
                "data": allocation_data,
                "response_time": round(time.time() - start_time, 3),
            }

        query = {}
        if employee_id:
            query["employee_id"] = employee_id
        if allocation_date:
            allocation_date_obj = datetime.strptime(allocation_date, '%Y-%m-%d').date()
            query["allocation_date"] = allocation_date_obj

        allocations = await db.allocations.find(query).to_list(length=None)

        for allocation in allocations:
            if "_id" in allocation:
                allocation["_id"] = str(allocation["_id"])
        
        return {
            "status_code": 200,
            "success_message": "success",
            "error_message": None,
            "data": allocations,
            "response_time": round(time.time() - start_time, 3),
        }

    except Exception as e:
        return {
            "status_code": 500,
            "success_message": None,
            "error_message": str(e),
            "data": None,
            "response_time": round(time.time() - start_time, 3)
        }
