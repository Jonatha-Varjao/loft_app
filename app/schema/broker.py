from typing import List, Optional

from pydantic import EmailStr

from app.schema.base import DBModelMixin
from app.schema.rwmodel import RWModel


class BrokerBase(RWModel):
    name: str
    email: EmailStr
    password: str
    celular: str
    idade: int
    creci: str

class BrokerInDB(DBModelMixin, BrokerBase):
    pass