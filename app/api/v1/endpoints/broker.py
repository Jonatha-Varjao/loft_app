from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, Query

from app.core.security import get_password_hash
from app.db.mongodb import AsyncIOMotorClient
from app.middleware.db import get_db
from app.schema.broker import BrokerBase, BrokerInDB
import app.crud.broker as broker_crud

router = APIRouter()

@router.post('/')
async def create_broker(
    db: AsyncIOMotorClient = Depends(get_db),
    *,
    broker_data: BrokerBase
) -> BrokerInDB :
    print('AAAAAAAAAAA')
    broker = await broker_crud.create(db, broker_in=broker_data)
    return broker


@router.get('/')
async def get_broker(
    db: AsyncIOMotorClient = Depends(get_db),
    limit: int = Query(10, gt=0),
    skip: int = Query(0, ge=0),
) -> List[BrokerInDB] :
    brokers: List[BrokerInDB] = []
    rows = db['hack']['brokers'].find(limit=limit, skip=skip)
    brokers = [ BrokerInDB(**row) async for row in rows ]
    return brokers