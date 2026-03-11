from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models import UserCreate, UserLogin, Token, UserOut
from app.database import (
    get_user_by_email, create_user, pwd_context,
    fake_users_db  # temporal, luego usaremos funciones
)
from app.exceptions import InvalidCredentialsException, ValidationException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Annotated
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.logger import log_login_attempt

# Configuración JWT (igual que antes)
SECRET_KEY = "ciclopuerto_2v_secret_key_2025B"  # Cámbiala después
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/auth", tags=["auth"])

# ============ FUNCIONES AUXILIARES ============

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ============ ENDPOINT DE REGISTRO ============

@router.post("/register", response_model=UserOut)
async def register(user_data: UserCreate):
    """
    Registra un nuevo usuario.
    Validaciones: email @alumnos.udg.mx, código numérico, password mínimo 6 caracteres.
    """
    # Verificar si el email ya existe
    if get_user_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Verificar si el código ya existe
    if user_data.codigo in fake_users_db:  # Por ahora buscamos en fake_db directamente
        raise HTTPException(status_code=400, detail="El código de alumno ya está registrado")
    
    # Hashear la contraseña
    hashed_password = get_password_hash(user_data.password)
    
    # Crear usuario
    new_user = {
        "codigo": user_data.codigo,
        "nombre": user_data.nombre,
        "email": user_data.email,
        "password": hashed_password,
        "rol": "estudiante"  # Por defecto
    }
    
    created_user = create_user(new_user)
    
    # No devolver la contraseña
    return UserOut(**created_user)

# ============ ENDPOINT DE LOGIN ============

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, user_credentials: UserLogin):
    client_ip = request.client.host if request.client else "unknown"
    
    try:
        # Buscar usuario por email
        user = get_user_by_email(user_credentials.email)
        
        if not user:
            log_login_attempt(
                email=user_credentials.email,
                success=False,
                client_ip=client_ip,
                details="Usuario no encontrado"
            )
            raise InvalidCredentialsException()
        
        if not verify_password(user_credentials.password, user["password"]):
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
        
        # Crear token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except ValueError as e:
        raise ValidationException(detail=str(e))

# ============ ENDPOINT PARA FORMULARIO OAuth2 (Documentación) ============

@router.post("/token", response_model=Token)
@limiter.limit("5/minute")
async def login_for_access_token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    client_ip = request.client.host if request.client else "unknown"
    
    user = get_user_by_email(form_data.username)
    
    if not user or not verify_password(form_data.password, user["password"]):
        log_login_attempt(
            email=form_data.username,
            success=False,
            client_ip=client_ip,
            details="Credenciales inválidas"
        )
        raise InvalidCredentialsException()
    
    log_login_attempt(
        email=form_data.username,
        success=True,
        client_ip=client_ip
    )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}