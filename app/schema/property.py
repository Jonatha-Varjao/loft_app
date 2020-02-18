from enum import Enum, IntEnum
from typing import List, Optional
from datetime import datetime

from pydantic import EmailStr, validator, Field
from bson import ObjectId

from app.schema.base import DateTimeModelMixin, DBModelMixin, Paginated, ObjectIdStr
from app.schema.rwmodel import RWModel


class Tipo(IntEnum):
    apartamento = 0
    casa = 1
    loft = 2
    terreno = 3

class Ambiente(IntEnum):
    praia = 0
    campo = 1
    urbano = 2
    periferia = 3

class Personalidade(IntEnum):
    familia = 0
    solteiros = 1
    temporada = 2
    fins = 3 
    comerciais = 4
    idosos = 5

class Valor(IntEnum):
    luxo = 0
    intermediario = 1
    popular = 2

class Plus(IntEnum):
    academia = 0
    lazer_adulto = 1
    lazer_idoso = 2 
    lazer_infatil = 3
    mobiliado = 4
    piscinas = 5
    portaria = 6
    esporte = 7
    imovel_novo = 8
    

class PropertyBase(DateTimeModelMixin, RWModel):
    nome: Optional[str]
    estado: Optional[str]
    cidade: Optional[str]
    dono: Optional[str] #object id do dono
    corretor: Optional[List[str]] #objects ids dos corretores
    tipo: Optional[Tipo]
    ambiente: Optional[Ambiente]
    personalidade: Optional[Personalidade]
    valor: Optional[Valor]
    plus: Optional[List[Plus]]
    geo_location: List = Field(..., min_items=2, max_items=2)

class PropertyInDB(DBModelMixin):
    nome: Optional[str]
    estado: Optional[str]
    cidade: Optional[str]
    dono: Optional[ObjectIdStr] # object id do dono
    corretor: Optional[List[str]] # objects ids dos corretores
    tipo: Optional[Tipo]
    ambiente: Optional[Ambiente]
    personalidade: Optional[Personalidade]
    valor: Optional[Valor]
    plus: Optional[List[Plus]]
    geo_location: List = Field(List, min_items=2, max_items=2)

    @validator("dono")
    def validate_id(cls, dono):
        return str(dono)

    class Config:
        allow_population_by_field_name = True
        json_encoders = { 
            ObjectId: lambda x: str(x)
        }


class PropertyUpdate(RWModel):
    nome: Optional[str]
    estado: Optional[str]
    cidade: Optional[str]
    dono: Optional[ObjectIdStr] # object id do dono
    corretor: Optional[List[str]] # objects ids dos corretores
    tipo: Optional[Tipo]
    ambiente: Optional[Ambiente]
    personalidade: Optional[Personalidade]
    valor: Optional[Valor]
    plus: Optional[List[Plus]]
    geo_location: Optional[List] = Field(None, min_items=2, max_items=2)


class PropertyList(Paginated):
    data: List[PropertyInDB]


    