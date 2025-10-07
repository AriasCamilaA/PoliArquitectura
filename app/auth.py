from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from typing import Dict

# Router de autenticación
router = APIRouter(prefix="/auth", tags=["auth"])

# Secret y configuración del token (en producción usar .env o vault)
SECRET_KEY = "CAMBIA_ESTO_POR_UN_SECRET_MUY_SEGUR0"  # cambiar para producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Simulación de usuarios (en prod usar DB)
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

_fake_users_db: Dict[str, Dict] = {
    "admin": {"username": "admin", "hashed_password": pwd_context.hash("adminpass"), "roles": ["admin"]},
    "user": {"username": "user", "hashed_password": pwd_context.hash("userpass"), "roles": ["client"]}
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain, hashed) -> bool:
    return pwd_context.verify(plain, hashed)

def authenticate_user(username: str, password: str):
    user = _fake_users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para login. Recibe username y password (form-data).
    Retorna token JWT para autenticación en endpoints protegidos.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    token = create_access_token({"sub": user["username"], "roles": user["roles"]})
    return {"access_token": token, "token_type": "bearer"}
