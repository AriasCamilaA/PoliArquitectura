from fastapi import APIRouter, HTTPException, Depends
from .models import reservations, rooms, next_reservation_id
from .schemas import ReservationCreate, Reservation
from .deps import get_current_user
from datetime import date

router = APIRouter(prefix="/reservas", tags=["reservas"])

@router.post("/", response_model=Reservation)
def create_reservation(payload: ReservationCreate, user=Depends(get_current_user)):
    """
    Flujo simplificado:
    - Verificar existencia de cliente y habitación (se asume cliente creado)
    - Verificar disponibilidad de habitación (flag 'available')
    - Crear reserva y marcar habitación no disponible
    - Retornar objeto reserva
    """
    # Validaciones básicas (en demo no verificamos cliente store)
    room = rooms.get(payload.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    if not room["available"]:
        raise HTTPException(status_code=400, detail="Habitación no disponible")
    # Crear reserva
    rid = next_reservation_id()
    res = {
        "id": rid,
        "client_id": payload.client_id,
        "room_id": payload.room_id,
        "from_date": payload.from_date,
        "to_date": payload.to_date,
        "status": "CONFIRMADA"
    }
    reservations[rid] = res
    # Marcar habitación no disponible (simplificado)
    room["available"] = False
    return res

@router.get("/{reservation_id}", response_model=Reservation)
def get_reservation(reservation_id: int, user=Depends(get_current_user)):
    r = reservations.get(reservation_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return r
