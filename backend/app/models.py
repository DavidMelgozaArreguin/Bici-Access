from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
from datetime import datetime
import re

# ============ MODELOS DE USUARIO ============

class UserCreate(BaseModel):
    """Modelo para registro de nuevo usuario"""
    codigo: str = Field(..., min_length=8, max_length=15, description="Código de alumno (ej: 2213522292)")
    nombre: str = Field(..., min_length=2, max_length=100)
    email: str
    password: str = Field(..., min_length=6)

    @validator('email')
    def validate_udg_email(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@alumnos\.udg\.mx$'
        if not re.match(pattern, v):
            raise ValueError('El email debe ser del dominio @alumnos.udg.mx')
        return v
    
    @validator('codigo')
    def validate_codigo(cls, v):
        if not v.isdigit() or len(v) < 8:
            raise ValueError('El código debe ser numérico y tener al menos 8 dígitos')
        return v

class UserLogin(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_udg_email(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@alumnos\.udg\.mx$'
        if not re.match(pattern, v):
            raise ValueError('El email debe ser del dominio @alumnos.udg.mx')
        return v

class UserOut(BaseModel):
    id: Optional[str] = None
    codigo: str
    nombre: str
    email: EmailStr
    rol: str = "estudiante"  # Por defecto estudiante
    fecha_registro: Optional[datetime] = None

    class Config:
        from_attributes = True

# ============ MODELOS DE BICICLETA ============

class BicicletaCreate(BaseModel):
    marca: str = Field(..., min_length=2, max_length=50)
    modelo: str = Field(..., min_length=2, max_length=50)
    color: str = Field(..., min_length=3, max_length=30)
    serial: str

    @validator('serial')
    def validate_serial_format(cls, v):
        # Formato: mínimo 5 caracteres, solo alfanuméricos y guiones
        if not re.match(r'^[A-Za-z0-9-]{5,}$', v):
            raise ValueError('El serial debe tener al menos 5 caracteres alfanuméricos (puede incluir guiones)')
        return v

class BicicletaOut(BicicletaCreate):
    id: str
    propietario_id: Optional[str] = None
    fecha_registro: Optional[datetime] = None
    activa: bool = True

    class Config:
        from_attributes = True

# ============ MODELOS DE REGISTRO ============

class RegistroCreate(BaseModel):
    bicicleta_id: str

class RegistroOut(BaseModel):
    id: str
    bicicleta_id: str
    usuario_id: Optional[str]
    usuario_nombre: str
    bicicleta_marca: str
    bicicleta_modelo: str
    fecha_entrada: datetime
    fecha_salida: Optional[datetime] = None
    activo: bool

    class Config:
        from_attributes = True

# ============ MODELOS DE TOKEN ============

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None