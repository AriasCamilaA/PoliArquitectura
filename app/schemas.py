from pydantic import BaseModel
from typing import Optional
from datetime import date

# --- Esquemas (request/response) ---

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserLogin(BaseModel):
    username: str
    password: str

class ClientCreate(BaseModel):
    name: str
    email: str

class Client(ClientCreate):
    id: int

class Room(BaseModel):
    id: int
    number: str
    type: str
    price: float
    available: bool

class ReservationCreate(BaseModel):
    client_id: int
    room_id: int
    from_date: date
    to_date: date

class Reservation(ReservationCreate):
    id: int
    status: str

class Invoice(BaseModel):
    id: int
    reservation_id: int
    amount: float
    issued_at: date
