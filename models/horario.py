from typing import Optional
from pydantic import BaseModel

class Horario(BaseModel):
    id: Optional[str]
    id_profesor: str
    id_materia: str
    nombre_profesor: str
    apellido_profesor: str
    nombre_materia: str
    hora_inicio: str
    hora_final: str