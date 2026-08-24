import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
DB_NAME = os.getenv("DB_NAME", "flyrent")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
rentals_collection = db["rentals"]
users_collection = db["users"]
