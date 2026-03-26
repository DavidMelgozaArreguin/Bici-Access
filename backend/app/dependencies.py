from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.database.usuarios import usuarios_collection
from app.config import SECRET_KEY, ALGORITHM 
from app.models import UserOut
from app.exceptions import PermissionDeniedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # LOG DE CONTROL: Esto saldrá en tu terminal de Python
        print(f"\n--- DEBUG AUTH ---")
        print(f"Token recibido: {token[:15]}...") 
        
        # 1. Decodifica el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        print(f"Email extraído: {email}")
        
        if email is None:
            print("ERROR: El payload no tiene 'sub'")
            raise credentials_exception
            
    except JWTError as e:
        print(f"ERROR JWT: {str(e)}")
        raise credentials_exception

    # 2. Buscar usuario en MongoDB
    # Si usas Motor (asíncrono), deja el await. Si usas PyMongo normal, quítalo.
    user_doc = usuarios_collection.find_one({"email": email}) 
    
    # Si el resultado es un objeto de Motor, hay que esperarlo:
    if hasattr(user_doc, "__await__"):
        user_doc = await user_doc

    print(f"Resultado DB: {'Usuario encontrado' if user_doc else 'No encontrado'}")

    if user_doc is None:
        raise credentials_exception

    # 3. Mapeo de datos
    user_data = {
        "id": str(user_doc["_id"]),
        "codigo": str(user_doc["codigo"]),
        "nombre": user_doc.get("nombre"),
        "email": user_doc.get("email"),
        "rol": user_doc.get("rol")
    }
    
    return UserOut(**user_data)

async def get_current_admin(current_user: UserOut = Depends(get_current_user)):
    if current_user.rol != "admin":
        raise PermissionDeniedException(
            detail="Se requieren privilegios de administrador para acceder a este recurso"
        )
    return current_user