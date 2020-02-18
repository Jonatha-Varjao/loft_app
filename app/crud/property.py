from datetime import datetime
from typing import List, Optional, Tuple

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
    await db['hack']['properties'].insert_one(property_json)
    property_json['_id']
    return property_json


async def get_by_id(
    db: AsyncIOMotorClient,
    *,
    property_id: str
) -> Optional[ PropertyInDB ] :
    
    property_data = await db['hack']['properties'].find_one({"_id": ObjectId(property_id)} )
    
    if not property_data:
        return None
    
    return property_data 

async def get_all_by_broker(
    db: AsyncIOMotorClient,
    *,
    broker_id: str,
    skip=0,
    limit=100,
    projections: {} = {}
) -> List[Optional[ Tuple[PropertyInDB, int] ]] :
    rows  =  db['hack']['properties'].find({"dono": ObjectId(broker_id)}, limit=limit, skip=skip)
    count = await db['hack']['properties'].count_documents({})
    properties = [ PropertyInDB(**row) async for row in rows ]
    return properties, count

async def get_all(
    db: AsyncIOMotorClient,
    *,
    skip=0,
    limit=100,
    projections: {} = {}
) -> List[Optional[ Tuple[PropertyInDB, int] ]] :
    rows  =  db['hack']['properties'].find(limit=limit, skip=skip)
    count = await db['hack']['properties'].count_documents({})
    properties = [ PropertyInDB(**row) async for row in rows ]
    return properties, count

async def delete(
    db: AsyncIOMotorClient,
    *,
    property_id: str
) -> Optional[PropertyInDB]:
    db['hack']['properties'].delete_one({"_id": ObjectId(property_id)})


async def update(
    db: AsyncIOMotorClient,
    property_data: PropertyUpdate,
    property_object: object, 
) -> PropertyUpdate:
    
    update_data = property_data.dict(skip_defaults=True)
    now = datetime.utcnow()
    update_data['updated_at'] = now
    
    await db['hack']['properties'].update_one(
        {"_id": ObjectId(property_object.id)}, 
        {"$set": update_data })
    
    return property_data
