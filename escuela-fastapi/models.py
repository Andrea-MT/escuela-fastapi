from pydantic import BaseModel, Field
from typing import Optional

class AlumnoBase(BaseModel):
    nombres: str = Field(min_length=1)
    apellidos: str = Field(min_length=1)
    matricula: str = Field(min_length=1)
    promedio: float = Field(ge=0.0, le=10.0)
    fotoPerfilUrl: Optional[str] = None
    
class AlumnoCreate(AlumnoBase):
    password: str = Field(min_length=1)

class Alumno(AlumnoBase):
    id: int
    password: Optional[str] = None
    class Config:
        orm_mode = True

class ProfesorBase(BaseModel):
    nombres: str = Field(min_length=1)
    apellidos: str = Field(min_length=1)
    numeroEmpleado: int = Field(gt=0)
    horasClase: int = Field(ge=0)

class ProfesorCreate(ProfesorBase):
    pass

class Profesor(ProfesorBase):
    id: int
    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    password: str

class VerifySessionRequest(BaseModel):
    sessionString: str

class LogoutRequest(BaseModel):
    sessionString: str
