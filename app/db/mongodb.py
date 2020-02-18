from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import GEO2D

from ..core.config import MONGODB_URI

class DataBase:
    client: AsyncIOMotorClient = None

db = DataBase()
db.client = AsyncIOMotorClient(MONGODB_URI)

db.client['hack']['brokers'].create_index( [("email", 1)], unique=True)
db.client['hack']['brokers'].create_index( [("phone", 1)], unique=True)
db.client['hack']['brokers'].create_index( [("creci", 1)], unique=True)
db.client['hack']['properties'].create_index( [("dono", 1)])
db.client['hack']['properties'].create_index([("geo_location", GEO2D)])