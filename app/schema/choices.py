
from app.schema.base import DBModelMixin
from app.schema.rwmodel import RWModel


class Choice(RWModel):
    pass

"""
TODO: Pensar na estrutura de dado melhor pra facilitar o cluster
proavelmente um dict/hash-table
"""