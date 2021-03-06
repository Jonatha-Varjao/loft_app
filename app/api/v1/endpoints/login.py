import json
from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.responses import Response

from app.middleware.db import get_db
from app.api.utils.security import get_current_user
from app.core import config
from app.core.jwt import create_access_token
from app.core.return_messages import codes, ptBr
from app.core.security import get_password_hash
from app.db.mongodb import AsyncIOMotorClient
from app.schema.token import LoginOAuth
from app.schema.broker import BrokerInDB

import app.crud.broker as broker_crud

router = APIRouter()


@router.post("/login/access-token")
async def login_access_token(
        *,
        db: AsyncIOMotorClient = Depends(get_db),
        data: LoginOAuth
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await broker_crud.authenticate(
        db, email=data.email, password=data.password
    )
    if not user:
        return Response(json.dumps({
            "messageCode": codes['validation'],
            "message": ptBr['eIncorrectDataLogin']
        }),
            status_code=401)
    
    user_response = {
        "id":str(user.id),
        "first_name":user.first_name,
        "last_name":user.last_name,
        "email":user.email
    }
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return {
            "access_token": create_access_token(
                data={
                    "user_data": user_response,
                },
                expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }

@router.post("/login/test-token", response_model=BrokerInDB)
def test_token(current_user: BrokerInDB = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user

