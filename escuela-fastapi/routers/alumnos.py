from fastapi import APIRouter, HTTPException, status
from typing import List
from models import Alumno, AlumnoCreate
from services import AlumnoService

router = APIRouter()
service = AlumnoService()

@router.get("", response_model=List[Alumno], status_code=status.HTTP_200_OK)
def list_alumnos():
    return service.get_all()

@router.get("/{id}", response_model=Alumno, status_code=status.HTTP_200_OK)
def get_alumno(id: int):
    alumno = service.get_by_id(id)
    if not alumno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")
    return alumno

@router.post("", response_model=Alumno, status_code=status.HTTP_201_CREATED)
def create_alumno(payload: Alumno):
    try:
        nuevo = service.create(payload)
        return nuevo
    except HTTPException as e:
        raise e

@router.put("/{id}", response_model=Alumno, status_code=status.HTTP_200_OK)
def update_alumno(id: int, payload: AlumnoCreate):
    updated = service.update(id, payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")
    return updated

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_alumno(id: int):
    deleted = service.delete(id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")
    return {"detail": "Alumno eliminado"}
