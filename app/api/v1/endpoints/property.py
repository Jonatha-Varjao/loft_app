import json
from typing import List, Optional


from bson import ObjectId
from fastapi import APIRouter, Depends, Query
from starlette.responses import Response

from app.core.excpetions import InvalidId
from app.core.return_messages import ptBr, codes
from app.db.mongodb import AsyncIOMotorClient
from app.middleware.db import get_db

from app.schema.property import PropertyBase, PropertyList, PropertyInDB, PropertyUpdate

import app.crud.property as property_crud

router = APIRouter()


@router.get('/')
async def get_all_properties(
    db: AsyncIOMotorClient = Depends(get_db),
    *,
    limit: int = Query(10, gt=0),
    skip: int = Query(0, ge=0),
    projections: dict = {}
) -> Optional[PropertyList] :
    properties, count = await property_crud.get_all(
        db,
        skip=skip,
        limit=limit,
        projections=projections
    )
    return PropertyList(data=properties, count=count)

@router.get('/{property_id}')
async def get_properties_by_id(
    db: AsyncIOMotorClient = Depends(get_db),
    *,
    property_id: str,
) -> Optional[PropertyInDB] :
    try:
        property_data = await property_crud.get_by_id(db, property_id=property_id)
    except InvalidId:
        return Response(json.dumps({
            "message": ptBr['eUserNotFound']
        }),status_code=404)
    
    if not property_data:
        return Response(json.dumps({
            "message": ptBr['eUserNotFound']
        }),status_code=404)
    
    return PropertyInDB(**property_data)

@router.put('/{property_id}')
async def update_property(
    db: AsyncIOMotorClient = Depends(get_db),
    *,
    property_id: str,
    property_data: PropertyUpdate,
) -> PropertyInDB : 
    
    if not property_data.dict(skip_defaults=True):
        return Response(json.dumps({
            "message": ptBr['formEmpty']
        }),status_code=422)
    
    property_object = await property_crud.get_by_id(db, property_id=property_id)
    if not property_object:
        return Response(json.dumps({
            "message": ptBr['eUserNotFound']
        }),
            status_code=404)
    
    updated_property = await property_crud.update(db, property_data=property_data, property_object=property_object)
    
    return updated_property

@router.delete('/{property_id}')
async def delete_property(
    db: AsyncIOMotorClient = Depends(get_db),
    *,
    property_id: str
) -> Optional[PropertyInDB] :
    try:
        property_object = await property_crud.get_by_id(db, property_id=property_id)
    except InvalidId:
        return Response(json.dumps({
            "message": ptBr['eUserNotFound']
        }),status_code=404)
    
    if not property_object:
        return Response(json.dumps({
            "message": ptBr['eUserNotFound']
        }),status_code=404)

    await property_crud.delete(db, property_id=property_id)

    return PropertyInDB(**property_object)