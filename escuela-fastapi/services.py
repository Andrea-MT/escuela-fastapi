from typing import List, Optional
from models import Alumno, AlumnoCreate, Profesor, ProfesorCreate

class AlumnoService:
    def __init__(self):
        self._alumnos: dict[int, Alumno] = {}
        self._next_id = 1

    def get_all(self) -> List[Alumno]:
        return list(self._alumnos.values())

    def get_by_id(self, id: int) -> Optional[Alumno]:
        return self._alumnos.get(id)

    def create(self, data: AlumnoCreate) -> Alumno:
        alumno = Alumno(id=self._next_id, **data.dict())
        self._alumnos[self._next_id] = alumno
        self._next_id += 1
        return alumno

    def update(self, id: int, data: AlumnoCreate) -> Optional[Alumno]:
        if id not in self._alumnos:
            return None
        alumno = Alumno(id=id, **data.dict())
        self._alumnos[id] = alumno
        return alumno

    def delete(self, id: int) -> bool:
        return self._alumnos.pop(id, None) is not None

class ProfesorService:
    def __init__(self):
        self._profesores: dict[int, Profesor] = {}
        self._next_id = 1

    def get_all(self) -> List[Profesor]:
        return list(self._profesores.values())

    def get_by_id(self, id: int) -> Optional[Profesor]:
        return self._profesores.get(id)

    def create(self, data: ProfesorCreate) -> Profesor:
        profesor = Profesor(id=self._next_id, **data.dict())
        self._profesores[self._next_id] = profesor
        self._next_id += 1
        return profesor

    def update(self, id: int, data: ProfesorCreate) -> Optional[Profesor]:
        if id not in self._profesores:
            return None
        profesor = Profesor(id=id, **data.dict())
        self._profesores[id] = profesor
        return profesor

    def delete(self, id: int) -> bool:
        return self._profesores.pop(id, None) is not None
