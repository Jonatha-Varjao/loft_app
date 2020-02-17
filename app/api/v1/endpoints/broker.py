import json
from typing import List, Optional


from bson import ObjectId
from fastapi import APIRouter, Depends, Query
from starlette.responses import Response

from app.core.excpetions import InvalidId
from app.core.return_messages import ptBr, codes
from app.core.security import get_password_hash
from app.db.mongodb import AsyncIOMotorClient
from app.middleware.db import get_db
from app.schema.broker import BrokerBase, BrokerInDB, BrokerUpdate, BrokerList

import app.crud.broker as broker_crud

router = APIRouter()

@router.post('/')
async def create_broker(
    db: AsyncIOMotorClient = Depends(get_db),
    *,
    broker_data: BrokerBase
) -> BrokerInDB :
    broker = await broker_crud.create(db, broker_in=broker_data)
    return BrokerInDB(**broker)

@router.put('/{broker_id}')
async def update_broker(
    db: AsyncIOMotorClient = Depends(get_db),
    *,
    broker_id: str,
    broker_data: BrokerUpdate,
) -> BrokerInDB :
    
    if not broker_data.dict(skip_defaults=True):
        return Response(json.dumps({
            "message": ptBr['formEmpty']
        }),status_code=422)
    
    broker = await broker_crud.get(db, broker_id=broker_id)
    if not broker:
        return Response(json.dumps({
            "message": ptBr['eUserNotFound']
        }),
            status_code=404)
    
    updated_broker = await broker_crud.update(db, broker_data=broker_data, broker=broker)
    
    return update_broker

@router.get('/')
async def get_broker(
    db: AsyncIOMotorClient = Depends(get_db),
    *,
    limit: int = Query(10, gt=0),
    skip: int = Query(0, ge=0),
    projections: dict = {}
) -> [Optional[BrokerList]] :
    brokers, count = await broker_crud.get_all(
        db,
        skip=skip,
        limit=limit,
        projections=projections
    )
    print(f'OUTER FUNCTION BROKERS {brokers}')
    print(f'OUTER FUNCTION COUNT {count}')
    return BrokerList(data=brokers, count=count)

@router.get('/{broker_id}')
async def get_broker(
    db: AsyncIOMotorClient = Depends(get_db),
    *,
    broker_id: str
) -> Optional[BrokerInDB] :
    try:
        broker = await broker_crud.get(db, broker_id=broker_id)
    except InvalidId:
        return Response(json.dumps({
            "message": ptBr['eUserNotFound']
        }),status_code=404)
    broker = await db['hack']['brokers'].find_one({"_id": ObjectId(broker_id) }, projection={'password': 0})
    
    if not broker:
        return Response(json.dumps({
            "message": ptBr['eUserNotFound']
        }),status_code=404)

    return BrokerInDB(**broker)

@router.delete('/{broker_id}')
async def delete_broker(
    db: AsyncIOMotorClient = Depends(get_db),
    *,
    broker_id: str
) -> Optional[BrokerInDB] :
    try:
        broker = await broker_crud.get(db, broker_id=broker_id)
    except InvalidId:
        return Response(json.dumps({
            "message": ptBr['eUserNotFound']
        }),status_code=404)
    
    if not broker:
        return Response(json.dumps({
            "message": ptBr['eUserNotFound']
        }),status_code=404)

    await broker_crud.delete(db, broker=broker)
    print('DELETE')
    return broker


