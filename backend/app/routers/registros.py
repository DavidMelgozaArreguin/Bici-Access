from fastapi import APIRouter, Depends, HTTPException
from app.models import RegistroCreate, RegistroOut, UserOut
from app.dependencies import get_current_user
from app.database import fake_registros_db, fake_bicicletas_db
from uuid import uuid4
from datetime import datetime

router = APIRouter(prefix="/registros", tags=["registros"])

# Registrar ENTRADA de una bicicleta
@router.post("/entrada", response_model=RegistroOut)
async def registrar_entrada(
    registro: RegistroCreate,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Registra la entrada de una bicicleta al ciclopuerto.
    La bicicleta debe pertenecer al usuario.
    """
    # 1. Verificar que la bicicleta exista
    bici = fake_bicicletas_db.get(registro.bicicleta_id)
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")
    
    # 2. Verificar que el usuario sea el propietario
    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No eres el propietario de esta bicicleta"
        )
    
    # 3. Verificar que la bicicleta no tenga ya un registro activo
    for reg_id, reg_data in fake_registros_db.items():
        if (reg_data["bicicleta_id"] == registro.bicicleta_id 
                and reg_data["activo"] == True):
            raise HTTPException(
                status_code=400,
                detail="Esta bicicleta ya se encuentra dentro del ciclopuerto"
            )
    
    # 4. Crear el nuevo registro
    registro_id = f"reg_{str(uuid4())[:8]}"
    nuevo_registro = {
        "id": registro_id,
        "bicicleta_id": registro.bicicleta_id,
        "usuario_id": current_user.id,
        "usuario_nombre": current_user.nombre,
        "bicicleta_marca": bici["marca"],
        "bicicleta_modelo": bici["modelo"],
        "fecha_entrada": datetime.now(),
        "fecha_salida": None,
        "activo": True
    }
    
    fake_registros_db[registro_id] = nuevo_registro
    return nuevo_registro

# Registrar SALIDA de una bicicleta
@router.post("/salida", response_model=RegistroOut)
async def registrar_salida(
    registro: RegistroCreate,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Registra la salida de una bicicleta del ciclopuerto.
    """
    # 1. Verificar que la bicicleta exista
    bici = fake_bicicletas_db.get(registro.bicicleta_id)
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")
    
    # 2. Verificar que el usuario sea el propietario
    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No eres el propietario de esta bicicleta"
        )
    
    # 3. Buscar un registro activo para esta bicicleta
    registro_activo = None
    registro_id_activo = None
    
    for reg_id, reg_data in fake_registros_db.items():
        if (reg_data["bicicleta_id"] == registro.bicicleta_id 
                and reg_data["activo"] == True):
            registro_activo = reg_data
            registro_id_activo = reg_id
            break
    
    if not registro_activo:
        raise HTTPException(
            status_code=400,
            detail="No hay un registro activo para esta bicicleta"
        )
    
    # 4. Marcar la salida
    registro_activo["fecha_salida"] = datetime.now()
    registro_activo["activo"] = False
    
    return registro_activo

# Listar registros ACTIVOS (bicicletas dentro del ciclopuerto)
@router.get("/activos", response_model=list[RegistroOut])
async def listar_registros_activos(
    current_user: UserOut = Depends(get_current_user)
):
    """
    Lista todas las bicicletas que se encuentran actualmente dentro del ciclopuerto.
    Solo muestra las bicicletas del usuario actual.
    """
    activos = []
    for reg_id, reg_data in fake_registros_db.items():
        if reg_data["usuario_id"] == current_user.id and reg_data["activo"] == True:
            activos.append(reg_data)
    
    return activos

# Historial de registros del usuario
@router.get("/mi-historial", response_model=list[RegistroOut])
async def obtener_mi_historial(
    current_user: UserOut = Depends(get_current_user)
):
    """
    Obtiene el historial completo de entradas/salidas del usuario.
    """
    historial = []
    for reg_id, reg_data in fake_registros_db.items():
        if reg_data["usuario_id"] == current_user.id:
            historial.append(reg_data)
    
    # Ordenar por fecha de entrada (más reciente primero)
    historial.sort(key=lambda x: x["fecha_entrada"], reverse=True)
    return historial