from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models import Alumno, AlumnoCreate, LoginRequest, VerifySessionRequest, LogoutRequest
from services import AlumnoService

router = APIRouter()
service = AlumnoService()

@router.get("", response_model=List[Alumno], status_code=status.HTTP_200_OK)
def list_alumnos(db: Session = Depends(get_db)):
    return service.get_all(db)

@router.get("/{id}", response_model=Alumno, status_code=status.HTTP_200_OK)
def get_alumno(id: int, db: Session = Depends(get_db)):
    alumno = service.get_by_id(db, id)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno

@router.post("", response_model=Alumno, status_code=status.HTTP_201_CREATED)
def create_alumno(payload: AlumnoCreate, db: Session = Depends(get_db)):
    return service.create(db, payload)

@router.put("/{id}", response_model=Alumno, status_code=status.HTTP_200_OK)
def update_alumno(id: int, payload: AlumnoCreate, db: Session = Depends(get_db)):
    updated = service.update(db, id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return updated

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_alumno(id: int, db: Session = Depends(get_db)):
    deleted = service.delete(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return {"detail": "Alumno eliminado"}

@router.post("/{id}/fotoPerfil", status_code=200)
def upload_foto_perfil(id: int, foto: UploadFile = File(...), db: Session = Depends(get_db)):
    url = service.upload_photo(db, id, foto)
    if not url:
         raise HTTPException(status_code=404, detail="Alumno no encontrado o error al subir")
    return {"fotoPerfilUrl": url, "message": "Foto subida exitosamente"}

@router.post("/{id}/email", status_code=200)
def send_email(id: int, db: Session = Depends(get_db)):
    sent = service.send_email_notification(db, id)
    if not sent:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return {"detail": "Correo enviado"}

@router.post("/{id}/session/login", status_code=200)
def session_login(id: int, payload: LoginRequest, db: Session = Depends(get_db)):
    session_string = service.login(db, id, payload.password)
    if not session_string:
         raise HTTPException(status_code=400, detail="Credenciales inválidas")
    return JSONResponse(status_code=200, content={"sessionString": session_string})

@router.post("/{id}/session/verify", status_code=200)
def session_verify(id: int, payload: VerifySessionRequest):
    is_valid = service.verify_session(id, payload.sessionString)
    if is_valid:
        return JSONResponse(status_code=200, content={"detail": "Sesión válida"})
    else:
        raise HTTPException(status_code=400, detail="Sesión inválida")

@router.post("/{id}/session/logout", status_code=200)
def session_logout(id: int, payload: LogoutRequest):
    success = service.logout(id, payload.sessionString)
    if not success:
        raise HTTPException(status_code=400, detail="Error al cerrar sesión")
    return JSONResponse(status_code=200, content={"detail": "Sesión cerrada"})

# @router.post("", response_model=Alumno, status_code=status.HTTP_201_CREATED)
# def create_alumno(payload: Alumno):
#     try:
#         nuevo = service.create(payload)
#         return nuevo
#     except HTTPException as e:
#         raise e

# @router.put("/{id}", response_model=Alumno, status_code=status.HTTP_200_OK)
# def update_alumno(id: int, payload: AlumnoCreate):
#     updated = service.update(id, payload)
#     if not updated:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")
#     return updated

# @router.delete("/{id}", status_code=status.HTTP_200_OK)
# def delete_alumno(id: int):
#     deleted = service.delete(id)
#     if not deleted:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")
#     return {"detail": "Alumno eliminado"}
