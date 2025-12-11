from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from routers import alumnos, profesores
import uvicorn
from database import engine, Base
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Escuela API - Cloud Foundations")

@app.get("/")
def read_root():
    return {"mensaje": "Dirígete a la ruta /alumnos o /profesores"}

@app.get("/health")
def health():
    return {"status": "healthy"}

app.include_router(alumnos.router, prefix="/alumnos", tags=["Alumnos"])
app.include_router(profesores.router, prefix="/profesores", tags=["Profesores"])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(), "body": exc.body}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})

@app.middleware("http")
async def method_not_allowed_middleware(request: Request, call_next):
    response = await call_next(request)
    return response

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=False)
