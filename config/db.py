# mongodb configuration

from motor.motor_asyncio import AsyncIOMotorClient
import os
import asyncio

mongo_uri = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
db_name = os.getenv("MONGO_DB_NAME", "vehicus") 
client = AsyncIOMotorClient(mongo_uri)
db = client[db_name]

# async def check_connection():
#     try:
#         await client.vehicus.command('ping')
#         print("Connected")
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     asyncio.run(check_connection())