# routers/profesores.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from models import Profesor, ProfesorCreate
from services import ProfesorService

router = APIRouter()
service = ProfesorService()

@router.get("/", response_model=List[Profesor], status_code=status.HTTP_200_OK)
def list_profesores():
    return service.get_all()

@router.get("/{id}", response_model=Profesor, status_code=status.HTTP_200_OK)
def get_profesor(id: int):
    profesor = service.get_by_id(id)
    if not profesor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
    return profesor

@router.post("/", response_model=Profesor, status_code=status.HTTP_201_CREATED)
def create_profesor(payload: ProfesorCreate):
    nuevo = service.create(payload)
    return nuevo

@router.put("/{id}", response_model=Profesor, status_code=status.HTTP_200_OK)
def update_profesor(id: int, payload: ProfesorCreate):
    updated = service.update(id, payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
    return updated

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_profesor(id: int):
    deleted = service.delete(id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")
    return {"detail": "Profesor eliminado"}
