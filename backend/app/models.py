from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import re
from typing import Optional
from datetime import datetime

# Configuración para todos los modelos
class CiclopuertoBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# -------------------- USUARIOS --------------------
class UserLogin(CiclopuertoBaseModel):
    email: str = Field(..., description="Email institucional (@alumnos.udg.mx)")
    password: str

    @field_validator('email')
    @classmethod
    def validate_udg_email(cls, v: str) -> str:
        pattern = r'^[a-zA-Z0-9._%+-]+@alumnos\.udg\.mx$'
        if not re.match(pattern, v):
            raise ValueError('El email debe ser del dominio @alumnos.udg.mx')
        return v

class UserOut(BaseModel):
    id: Optional[int] = None
    codigo: str
    nombre: str
    email: EmailStr
    rol: str  

    class Config:
        from_attributes = True


# -------------------- BICICLETAS --------------------
class BicicletaCreate(CiclopuertoBaseModel):
    marca: str = Field(..., min_length=2, max_length=50)
    modelo: str = Field(..., min_length=2, max_length=50)
    color: str = Field(..., min_length=3, max_length=30)
    serial: str = Field(..., min_length=5, max_length=50)

    @field_validator('serial')
    @classmethod
    def validate_serial_format(cls, v: str) -> str:
        # Formato: mínimo 5 caracteres, solo alfanuméricos y guiones
        if not re.match(r'^[A-Za-z0-9-]{5,}$', v):
            raise ValueError('El serial debe tener al menos 5 caracteres alfanuméricos (puede incluir guiones)')
        return v

class BicicletaOut(BicicletaCreate):
    id: str
    propietario_id: int

# -------------------- REGISTROS --------------------
class RegistroBase(CiclopuertoBaseModel):
    bicicleta_id: str

class RegistroCreate(RegistroBase):
    pass

class RegistroOut(RegistroBase):
    id: str
    usuario_id: int
    usuario_nombre: str
    bicicleta_marca: str
    bicicleta_modelo: str
    fecha_entrada: datetime
    fecha_salida: Optional[datetime] = None
    activo: bool

# -------------------- TOKENS --------------------
class Token(CiclopuertoBaseModel):
    access_token: str
    token_type: str

class TokenData(CiclopuertoBaseModel):
    email: Optional[str] = None