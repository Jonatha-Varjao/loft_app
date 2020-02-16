from typing import List, Optional
from datetime import datetime
from pydantic import EmailStr

from app.schema.base import DBModelMixin
from app.schema.rwmodel import RWModel

class BrokerBase(RWModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str
    idade: int
    creci: str
    created_at: datetime = None
    update_at: datetime = None

class BrokerInDB(DBModelMixin):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    idade: int
    creci: str
    created_at: datetime = None
    update_at: datetime = None
    

class BrokerUpdate(RWModel):
    first_name: str
    last_name: str
    idade: int
    creci: str
    update_at: datetime = None