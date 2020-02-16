from datetime import datetime
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from app.db.mongodb import AsyncIOMotorClient

from app.core.security import get_password_hash, verify_password
from app.schema.broker import BrokerInDB, BrokerBase


async def get(db: AsyncIOMotorClient, user_id: str) -> Optional[BrokerInDB]:
    broker = db['hack']['brokers'].find_one({"_id":ObjectId(id) })
    return BrokerInDB(**broker)


async def get_by_email(db: AsyncIOMotorClient, *, email: str) -> Optional[BrokerInDB]:
    broker = db['hack']['brokers'].find_one({"email": email })
    return BrokerInDB(**broker)

async def authenticate(db: AsyncIOMotorClient, *, email: str, password: str) -> Optional[BrokerInDB]:
    user = await get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


async def get_multi(
    db: AsyncIOMotorClient,
    *,
    skip=0,
    limit=100,
    environment: str
    ) -> List[Optional[BrokerInDB]]:
    return  

async def get_all_multi(db: AsyncIOMotorClient, *, skip=0, limit=100) -> List[Optional[BrokerInDB]]:
    return  db.query(BrokerInDB)\
        .order_by(BrokerInDB.full_name)\
        .offset(skip)\
        .limit(limit)\
        .all()

async def create(db: AsyncIOMotorClient, *, broker_in: BrokerBase) -> BrokerInDB:
    broker_in.password = get_password_hash(broker_in.password)
    now = datetime.utcnow()
    broker_in.created_at, broker_in.update_at = now, now
    broker_json = broker_in.dict()
    await db['hack']['brokers'].insert_one(broker_json) 
    broker_json['_id']
    return broker_json



async def update(db: AsyncIOMotorClient) -> BrokerInDB:
    user_data = jsonable_encoder(user)
    update_data = user_in.dict(skip_defaults=True)
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])
    if user_in.password:
        passwordhash = get_password_hash(user_in.password)
        user.password = passwordhash
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user
