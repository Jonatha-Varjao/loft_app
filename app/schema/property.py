from enum import Enum, IntEnum
from typing import List, Optional
from datetime import datetime
from pydantic import EmailStr

from app.schema.base import DateTimeModelMixin, DBModelMixin, Paginated
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
    
    dono: str #object id do dono
    corretor: List[str] #objects ids dos corretores
    tipo: Tipo
    ambiente: Ambiente
    personalidade: Personalidade
    valor: Valor
    plus: List[Plus]
    
    

class PropertyInDB(DBModelMixin):
    pass

class PropertyUpdate(RWModel):
    pass

class PropertyList(Paginated):
    data: List[PropertyInDB]


    