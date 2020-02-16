from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from app.db.mongodb import AsyncIOMotorClient

from app.core.security import get_password_hash, verify_password
from app.schema.broker import BrokerInDB, BrokerBase


async def get(db_session: AsyncIOMotorClient, user_id: str) -> Optional[BrokerInDB]:
    return  


async def get_by_email(db_session: AsyncIOMotorClient, *, email: str) -> Optional[BrokerInDB]:
    return  


async def get_by_username(db_session: AsyncIOMotorClient, *, username: str) -> Optional[BrokerInDB]:
    return  


async def authenticate(db_session: AsyncIOMotorClient, *, email_or_username: str, password: str) -> Optional[BrokerInDB]:
    user
    if not user:
        user
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


async def get_multi(
    db_session: AsyncIOMotorClient,
    *,
    skip=0,
    limit=100,
    environment: str
    ) -> List[Optional[BrokerInDB]]:
    return  

async def get_all_multi(db_session: AsyncIOMotorClient, *, skip=0, limit=100) -> List[Optional[BrokerInDB]]:
    return  db_session.query(BrokerInDB)\
        .order_by(BrokerInDB.full_name)\
        .offset(skip)\
        .limit(limit)\
        .all()

async def create(db_session: AsyncIOMotorClient, *, user_in: BrokerBase) -> BrokerInDB:
    user = BrokerInDB(
        **user_in.dict()
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user


async def update(db_session: AsyncIOMotorClient) -> BrokerInDB:
    user_data = jsonable_encoder(user)
    update_data = user_in.dict(skip_defaults=True)
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])
    if user_in.password:
        passwordhash = get_password_hash(user_in.password)
        user.password = passwordhash
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user
