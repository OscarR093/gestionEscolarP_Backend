from typing import Optional
from pydantic import BaseModel

class Maestro(BaseModel):
    id: Optional[str]
    nombre: str
    apellido: str
    direccion: str
    telefono:str