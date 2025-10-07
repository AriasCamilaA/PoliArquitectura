from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from .auth import oauth2_scheme, SECRET_KEY, ALGORITHM

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependencia para obtener el usuario actual desde el token JWT.
    Lanza excepción si el token es inválido o expiró.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        roles = payload.get("roles", [])
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"username": username, "roles": roles}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
