from pydantic import BaseModel, Field

class Alumno(BaseModel):
    id: int
    nombres: str = Field(min_length=1)
    apellidos: str = Field(min_length=1)
    matricula: str = Field(min_length=1)
    promedio: float = Field(ge=0.0, le=10.0)

class AlumnoCreate(BaseModel):
    nombres: str = Field(min_length=1)
    apellidos: str = Field(min_length=1)
    matricula: str = Field(min_length=1)
    promedio: float = Field(ge=0.0, le=10.0)

class Profesor(BaseModel):
    id: int
    nombres: str = Field(min_length=1)
    apellidos: str = Field(min_length=1)
    numeroEmpleado: int
    horasClase: int = Field(ge=0)

class ProfesorCreate(BaseModel):
    id: int
    nombres: str = Field(min_length=1)
    apellidos: str = Field(min_length=1)
    numeroEmpleado: int
    horasClase: int = Field(ge=0)
