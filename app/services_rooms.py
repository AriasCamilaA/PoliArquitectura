from fastapi import APIRouter, HTTPException
from .models import rooms
from .schemas import Room

router = APIRouter(prefix="/habitaciones", tags=["habitaciones"])

@router.get("/disponibles", response_model=list[Room])
def get_available_rooms():
    """
    Retorna habitaciones marcadas como disponibles.
    Endpoint público (para demo). En producción se puede proteger.
    """
    return [r for r in rooms.values() if r["available"]]

@router.get("/", response_model=list[Room])
def list_rooms():
    return list(rooms.values())
