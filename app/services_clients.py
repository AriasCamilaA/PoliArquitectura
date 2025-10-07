from fastapi import APIRouter, HTTPException, Depends
from .schemas import ClientCreate, Client
from .models import clients, next_client_id
from .deps import get_current_user

router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.post("/", response_model=Client)
def create_client(payload: ClientCreate, user=Depends(get_current_user)):
    """
    Crear cliente. Requiere token (usuario autenticado).
    """
    cid = next_client_id()
    client = {"id": cid, "name": payload.name, "email": payload.email}
    clients[cid] = client
    return client

@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int, user=Depends(get_current_user)):
    client = clients.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

@router.get("/", response_model=list[Client])
def list_clients(user=Depends(get_current_user)):
    return list(clients.values())
