from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.database import fake_users_db, SECRET_KEY, ALGORITHM
from app.models import UserOut
from app.exceptions import PermissionDeniedException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        #Decodifica el token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    #Busca el usuario por email en base de datos temporal
    user = None
    for user_key, user_data in fake_users_db.items():
        if user_data["email"] == email:
            user = user_data
            break

    if user is None:
        raise credentials_exception
        
    #Devuelve el usuario usando el modelo UserOut (sin password)
    return UserOut(**user)

async def get_current_admin(current_user: UserOut = Depends(get_current_user)):
    """
    Dependencia que verifica si el usuario actual es administrador.
    Si no es admin, lanza un error 403.
    """
    if current_user.rol != "admin":
        raise PermissionDeniedException(
            detail="Se requieren privilegios de administrador para acceder a este recurso"
        )
    return current_user
