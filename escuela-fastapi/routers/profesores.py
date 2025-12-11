from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models import Profesor, ProfesorCreate
from services import ProfesorService

router = APIRouter()
service = ProfesorService()

@router.get("", response_model=List[Profesor], status_code=200)
def list_profesores(db: Session = Depends(get_db)):
    return service.get_all(db)

@router.get("/{id}", response_model=Profesor, status_code=200)
def get_profesor(id: int, db: Session = Depends(get_db)):
    profesor = service.get_by_id(db, id)
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor

@router.post("", response_model=Profesor, status_code=201)
def create_profesor(payload: ProfesorCreate, db: Session = Depends(get_db)):
    try:
        return service.create(db, payload)
    except:
        raise HTTPException(status_code=400, detail="Profesor ya existe")

@router.put("/{id}", response_model=Profesor, status_code=200)
def update_profesor(id: int, payload: ProfesorCreate, db: Session = Depends(get_db)):
    updated = service.update(db, id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return updated

@router.delete("/{id}", status_code=200)
def delete_profesor(id: int, db: Session = Depends(get_db)):
    deleted = service.delete(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return {"detail": "Profesor eliminado"}
