from sqlalchemy import Column, Integer, String, Float
from database import Base

class AlumnoDB(Base):
    __tablename__ = "alumnos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombres = Column(String(100))
    apellidos = Column(String(100))
    matricula = Column(String(50))
    promedio = Column(Float)
    fotoPerfilUrl = Column(String(255), nullable=True)
    password = Column(String(100), nullable=True)

class ProfesorDB(Base):
    __tablename__ = "profesores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombres = Column(String(100))
    apellidos = Column(String(100))
    numeroEmpleado = Column(Integer)
    horasClase = Column(Integer)