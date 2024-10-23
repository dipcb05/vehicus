import uvicorn
import os
from pymongo import MongoClient
from api.index import app

# MongoDB connection details
mongo_uri = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
mongo_db_name = os.getenv("MONGO_DB_NAME", "vehicus")
client = MongoClient(mongo_uri)
db = client[mongo_db_name]

#check if db is seed already
def is_db_empty():
    vehicles_collection = db.vehicles.find_one()
    drivers_collection = db.drivers.find_one()
    return vehicles_collection is None and drivers_collection is None

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))

#seed only for first time
    if is_db_empty():
        from config.seed import populate_data
        populate_data(1000)
    uvicorn.run(app, host=host, port=port)
