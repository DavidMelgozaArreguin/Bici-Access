from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.models import UserLogin, Token
from app.database import fake_users_db, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.exceptions import InvalidCredentialsException, ValidationException
from app.logger import log_login_attempt
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from slowapi import Limiter
from slowapi.util import get_remote_address

# Configurar limiter para este router
limiter = Limiter(key_func=get_remote_address)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/auth", tags=["auth"])

# Función para verificar la contraseña plana contra el hash guardado
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ENDPOINT PRINCIPAL DE LOGIN (ahora devuelve un Token)
@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, user_credentials: UserLogin):
    """
    Endpoint para iniciar sesión.
    Límite: 5 intentos por minuto por IP.
    """
    client_ip = request.client.host if request.client else "unknown"
    
    try:
        # Validación automática con Pydantic V2 (ya está en el modelo)
        
        # Buscar usuario
        user_found = None
        for user_key, user_data in fake_users_db.items():
            if user_data["email"] == user_credentials.email:
                user_found = user_data
                break

        # Usuario no encontrado
        if not user_found:
            log_login_attempt(
                email=user_credentials.email,
                success=False,
                client_ip=client_ip,
                details="Usuario no encontrado"
            )
            raise InvalidCredentialsException()

        # Contraseña incorrecta
        if not verify_password(user_credentials.password, user_found["password"]):
            log_login_attempt(
                email=user_credentials.email,
                success=False,
                client_ip=client_ip,
                details="Contraseña incorrecta"
            )
            raise InvalidCredentialsException()

        # Login exitoso
        log_login_attempt(
            email=user_credentials.email,
            success=True,
            client_ip=client_ip
        )

        # Crear token JWT
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_found["email"]}, 
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
        
    except ValueError as e:
        # Captura errores de validación de Pydantic
        log_login_attempt(
            email=user_credentials.email,
            success=False,
            client_ip=client_ip,
            details=f"Error validación: {str(e)}"
        )
        raise ValidationException(detail=str(e))
    
    except Exception as e:
        # Cualquier otro error
        log_login_attempt(
            email=user_credentials.email,
            success=False,
            client_ip=client_ip,
            details=f"Error inesperado: {str(e)}"
        )
        # Re-lanzamos la excepción original
        raise

# ENDPOINT PARA EL FORMULARIO DE LA DOCUMENTACIÓN
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para login con OAuth2 (formulario estándar).
    Usado por la documentación interactiva de FastAPI.
    """
    # Buscar usuario
    user_found = None
    for user_key, user_data in fake_users_db.items():
        if user_data["email"] == form_data.username:  # OAuth2 usa 'username' para email
            user_found = user_data
            break

    if not user_found or not verify_password(form_data.password, user_found["password"]):
        raise InvalidCredentialsException()

    # Crear token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_found["email"]}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}