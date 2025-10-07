from fastapi import FastAPI
from .auth import router as auth_router
from .services_clients import router as clients_router
from .services_rooms import router as rooms_router
from .services_reservations import router as reservations_router
from .services_billing import router as billing_router

app = FastAPI(title="Hotel API - Entrega 3", version="0.1")

# Incluir routers
app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(rooms_router)
app.include_router(reservations_router)
app.include_router(billing_router)

@app.get("/")
def root():
    return {"message": "API Hotel - Entrega 3. Ver /docs para documentación OpenAPI"}
