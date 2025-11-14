from fastapi import APIRouter, HTTPException
from typing import List
from models import Profesor, ProfesorCreate
from services import ProfesorService

router = APIRouter()
service = ProfesorService()

@router.get("", response_model=List[Profesor], status_code=200)
def list_profesores():
    return service.get_all()

@router.get("/{id}", response_model=Profesor, status_code=200)
def get_profesor(id: int):
    profesor = service.get_by_id(id)
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor

@router.post("", response_model=Profesor, status_code=201)
def create_profesor(payload: Profesor):
    try:
        return service.create(payload)
    except:
        raise HTTPException(status_code=400, detail="Profesor ya existe")

@router.put("/{id}", response_model=Profesor, status_code=200)
def update_profesor(id: int, payload: ProfesorCreate):
    updated = service.update(id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return updated

@router.delete("/{id}", status_code=200)
def delete_profesor(id: int):
    deleted = service.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return {"detail": "Profesor eliminado"}
