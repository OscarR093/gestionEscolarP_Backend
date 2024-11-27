from pydantic import BaseModel
from typing import Optional

class Materia(BaseModel):
    id: Optional[str]
    nombre: str
    HoraInicio: str
    HoraFinal: str
    Asignada: bool
