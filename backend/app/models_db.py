"""
Modelos de Base de Datos para MongoDB.
Estos modelos definen la estructura exacta de las colecciones.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

# Clase especial para manejar ObjectId de MongoDB
class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return str(v)

# Usuario en la base de datos
class UsuarioDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    codigo: str = Field(..., min_length=8, max_length=15)  
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str  # Hash bcrypt
    fecha_registro: datetime = Field(default_factory=datetime.now)
    activo: bool = True

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Bicicleta en la base de datos
class BicicletaDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    propietario_id: str  # ID del usuario (referencia a UsuarioDB)
    marca: str = Field(..., min_length=2, max_length=50)
    modelo: str = Field(..., min_length=2, max_length=50)
    color: str = Field(..., min_length=3, max_length=30)
    serial: str = Field(..., min_length=5, max_length=50, unique=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)
    activa: bool = True  # Para eliminacion logica

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Registro de entrada/salida en la base de datos
class RegistroDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    bicicleta_id: str  # ID de la bicicleta (referencia a BicicletaDB)
    usuario_id: str    # ID del usuario que realizó el registro (referencia a UsuarioDB)
    usuario_nombre: str  # Caché del nombre para no hacer join siempre
    bicicleta_marca: str  # Caché de la marca
    bicicleta_modelo: str  # Caché del modelo
    tipo: str = Field(..., regex="^(entrada|salida)$")  # Solo puede ser "entrada" o "salida"
    fecha: datetime = Field(default_factory=datetime.now)
    # Para entrada: no tiene fecha_fin, para salida: sí tiene
    fecha_fin: Optional[datetime] = None
    activo: bool = True  # Un registro de entrada está activo hasta que tenga una salida

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}