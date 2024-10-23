import random
import string
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

mongo_uri = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
mongo_db_name = os.getenv("MONGO_DB_NAME", "vehicus")
client = MongoClient(mongo_uri)
db = client[mongo_db_name]

def generate_random_data(num_records):
    vehicles = []
    drivers = []

    for i in range(num_records):
        vehicle_id = str(ObjectId())
        driver_id = str(ObjectId())
        
        vehicles.append({
            "_id": ObjectId(vehicle_id),
            "vehicle_id": vehicle_id,
            "driver_id": driver_id,
            "model": f"Model_{i+1}",
            "license_plate": ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        })
        
        drivers.append({
            "_id": ObjectId(driver_id),
            "driver_id": driver_id,
            "name": f"Driver_{i+1}",
            "license_number": f"L12345{i+1}",
            "contact_info": f"123-456-78{str(i).zfill(2)}"
        })
    
    return vehicles, drivers

def populate_data(num_records):
    vehicles, drivers = generate_random_data(num_records)    
    db.vehicles.insert_many(vehicles)
    db.drivers.insert_many(drivers)

if __name__ == "__main__":
    populate_data(1000)
