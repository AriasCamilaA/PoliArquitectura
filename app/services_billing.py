from fastapi import APIRouter, HTTPException, Depends
from .models import reservations, invoices, next_invoice_id
from .schemas import Invoice
from datetime import date
from .deps import get_current_user

router = APIRouter(prefix="/facturacion", tags=["facturacion"])

@router.post("/emitir/{reservation_id}", response_model=Invoice)
def issue_invoice(reservation_id: int, user=Depends(get_current_user)):
    """
    Genera una factura simplificada a partir de la reserva.
    """
    res = reservations.get(reservation_id)
    if not res:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    # Calcular monto básico (en demo simple: days * room.price)
    # Nota: en este demo no accedemos directamente al precio; se podría agregar
    invoice_id = next_invoice_id()
    inv = {"id": invoice_id, "reservation_id": reservation_id, "amount": 100.0, "issued_at": date.today()}
    invoices[invoice_id] = inv
    return inv

@router.get("/{invoice_id}", response_model=Invoice)
def get_invoice(invoice_id: int, user=Depends(get_current_user)):
    inv = invoices.get(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return inv
