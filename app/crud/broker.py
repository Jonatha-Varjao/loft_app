from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from app.db.mongodb import AsyncIOMotorClient
from app.core.security import get_password_hash, verify_password
from app.schema.broker import BrokerInDB, BrokerBase, BrokerUpdate


async def get(
    db: AsyncIOMotorClient,
    *,
    broker_id: str,
    projections: {} = {},
    filters: {} = {}
) -> Optional[BrokerInDB]:
    broker = await db['hack']['brokers'].find_one(
        {"_id": ObjectId(broker_id), **filters },
        projection={'password': 0, **projections})
    
    if not broker:
        return None

    return BrokerInDB(**broker)


async def get_by_email(db: AsyncIOMotorClient, *, email: str) -> Optional[BrokerInDB]:
    broker = await db['hack']['brokers'].find_one({"email": email })
    
    if not broker:
        return None
    
    return BrokerInDB(**broker)

async def authenticate(db: AsyncIOMotorClient, *, email: str, password: str) -> Optional[BrokerInDB]:
    user = await get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


async def update(
    db: AsyncIOMotorClient,
    broker_data: BrokerUpdate,
    broker: object, 
) -> BrokerInDB:
    update_data = broker_data.dict(skip_defaults=True)

    if "password" in broker_data:
        passwordhash = get_password_hash(broker['password'])
        broker['password'] = passwordhash
    
    now = datetime.utcnow()
    update_data['updated_at'] = now

    await db['hack']['brokers'].update_one({"_id": broker.id},{"$set": update_data } )
    return broker

async def get_all(
    db: AsyncIOMotorClient,
    *,
    skip=0,
    limit=100,
    projections: {} = {}
) -> List[Optional[BrokerInDB]]:
    rows  =  db['hack']['brokers'].find(limit=limit, skip=skip, projection={'password': 0, **projections})
    count = await db['hack']['brokers'].count_documents({})
    brokers = [ BrokerInDB(**row) async for row in rows ]
    print(f'INNER FUNCTION BROKERS {brokers}')
    print(f'INNER FUNCTION COUNT {count}')
    return brokers, count

async def create(db: AsyncIOMotorClient, *, broker_in: BrokerBase) -> BrokerInDB:
    print(broker_in)
    broker_in.password = get_password_hash(broker_in.password)
    now = datetime.utcnow()
    broker_in.created_at, broker_in.updated_at = now, now
    broker_json = broker_in.dict()
    await db['hack']['brokers'].insert_one(broker_json) 
    broker_json['_id']
    return broker_json


async def delete(
    db: AsyncIOMotorClient, 
    *,
    broker: object
):
    db['hack']['brokers'].delete_one({"_id": ObjectId(broker.id)})
    