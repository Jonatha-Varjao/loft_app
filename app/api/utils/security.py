from jwt import PyJWTError
import jwt

from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import Response

import app.crud.broker as crud_broker
from app.middleware.db import get_db
from app.core import config
from app.core.jwt import ALGORITHM
from app.db.mongodb import AsyncIOMotorClient
from app.schema.broker import BrokerInDB
from app.schema.token import TokenPayload
from app.core.return_messages import codes, ptBr


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")

def get_current_user(
    db: AsyncIOMotorClient = Depends(get_db),
    token: str = Security(reusable_oauth2)
    ):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Token expirou/invalido"
        )
    user # = GRAB USER FROM DB

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

