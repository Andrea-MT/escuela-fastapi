from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from routers import alumnos, profesores
import uvicorn

app = FastAPI(title="Escuela API - FastAPI")

@app.get("/")
def read_root():
    return {"mensaje": "Dirígete a la ruta /alumnos o /profesores"}

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
