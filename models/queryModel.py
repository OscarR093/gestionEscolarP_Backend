from pydantic import BaseModel
from typing import Union

class QueryModel(BaseModel):
    field: str  # Campo por el cual se buscará
    value: Union[str, bool]  # Valor que debe coincidir con el campo
