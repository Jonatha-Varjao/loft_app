from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from app.db.mongodb import AsyncIOMotorClient
from app.core.security import get_password_hash, verify_password

from app.schema.property import PropertyBase, PropertyInDB, PropertyList, PropertyUpdate

async def create(
    db: AsyncIOMotorClient,
    *,
    broker_id: str,
    property_in: PropertyBase
) -> PropertyInDB:
    now = datetime.utcnow()
    property_in.created_at, property_in.updated_at = now, now
    property_in.dono = ObjectId(broker_id)
    property_json = property_in.dict()
    print('bbbbbbbbbb ', property_json)
    await db['hack']['properties'].insert_one(property_json)
    property_json['_id']
    return property_json

