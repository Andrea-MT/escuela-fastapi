from pydantic import BaseModel, Field, conint, confloat
from typing import Optional

class AlumnoCreate(BaseModel):
    nombres: str = Field(..., min_length=1, description="Nombres del alumno")
    apellidos: str = Field(..., min_length=1, description="Apellidos del alumno")
    matricula: str = Field(..., min_length=1, description="Matrícula")
    promedio: confloat(ge=0.0, le=100.0) = Field(..., description="Promedio entre 0 y 100")

class Alumno(AlumnoCreate):
    id: int

class ProfesorCreate(BaseModel):
    numeroEmpleado: conint(gt=0) = Field(..., description="Número de empleado (entero positivo)")
    nombres: str = Field(..., min_length=1, description="Nombres del profesor")
    apellidos: str = Field(..., min_length=1, description="Apellidos del profesor")
    horasClase: conint(ge=1) = Field(..., description="Horas de clase (al menos 1)")

class Profesor(ProfesorCreate):
    id: int
