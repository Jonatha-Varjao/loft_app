from typing import List, Optional
from datetime import datetime
from pydantic import EmailStr

from app.schema.base import DateTimeModelMixin, DBModelMixin, Paginated
from app.schema.rwmodel import RWModel

class BrokerBase(DateTimeModelMixin, RWModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str
    idade: int
    creci: str

class BrokerInDB(DBModelMixin):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    idade: int
    creci: str
    

class BrokerUpdate(RWModel):
    first_name: Optional[str]
    last_name: Optional[str]
    idade: Optional[int]
    creci: Optional[str]

class BrokerList(Paginated):
    data: List[BrokerInDB]