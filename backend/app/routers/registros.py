from fastapi import APIRouter, Depends, HTTPException, Request
from app.models import RegistroCreate, RegistroOut, UserOut
from app.dependencies import get_current_user
from app.database import (
    get_bicicleta_by_id,
    get_registro_activo_by_bicicleta,
    create_registro_entrada,
    update_registro_salida,
    get_registros_activos_by_usuario,
    get_registros_by_usuario
)
from app.logger import log_registro_event

router = APIRouter(prefix="/registros", tags=["registros"])

# ============ ENTRADA ============

@router.post("/entrada", response_model=RegistroOut)
async def registrar_entrada(
    request: Request,
    registro: RegistroCreate,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Registra la entrada de una bicicleta.
    La bicicleta debe pertenecer al usuario y no tener un registro activo.
    """
    # Verificar bicicleta
    bici = get_bicicleta_by_id(registro.bicicleta_id)
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")
    
    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No eres el propietario de esta bicicleta"
        )
    
    # Verificar que no tenga registro activo
    activo = get_registro_activo_by_bicicleta(registro.bicicleta_id)
    if activo:
        raise HTTPException(
            status_code=400,
            detail="Esta bicicleta ya se encuentra dentro del ciclopuerto"
        )
    
    # Crear registro
    nuevo_registro = {
        "bicicleta_id": registro.bicicleta_id,
        "usuario_id": current_user.id,
        "usuario_nombre": current_user.nombre,
        "bicicleta_marca": bici["marca"],
        "bicicleta_modelo": bici["modelo"]
    }
    
    registro_creado = create_registro_entrada(nuevo_registro)
    
    log_registro_event("entrada", registro_creado["id"], current_user.id, request.client.host)
    
    return registro_creado

# ============ SALIDA ============

@router.post("/salida", response_model=RegistroOut)
async def registrar_salida(
    request: Request,
    registro: RegistroCreate,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Registra la salida de una bicicleta.
    La bicicleta debe tener un registro activo.
    """
    # Verificar bicicleta
    bici = get_bicicleta_by_id(registro.bicicleta_id)
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")
    
    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No eres el propietario de esta bicicleta"
        )
    
    # Buscar registro activo
    activo = get_registro_activo_by_bicicleta(registro.bicicleta_id)
    if not activo:
        raise HTTPException(
            status_code=400,
            detail="No hay un registro activo para esta bicicleta"
        )
    
    # Actualizar salida
    registro_actualizado = update_registro_salida(activo["id"])
    
    log_registro_event("salida", registro_actualizado["id"], current_user.id, request.client.host)
    
    return registro_actualizado

# ============ ACTIVOS (bicis dentro) ============

@router.get("/activos", response_model=list[RegistroOut])
async def listar_registros_activos(
    request: Request,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Lista las bicicletas del usuario que están actualmente dentro.
    """
    activos = get_registros_activos_by_usuario(current_user.id)
    return activos

# ============ HISTORIAL ============

@router.get("/mi-historial", response_model=list[RegistroOut])
async def obtener_mi_historial(
    request: Request,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Obtiene el historial completo de entradas/salidas del usuario.
    """
    historial = get_registros_by_usuario(current_user.id)
    # Ordenar por fecha descendente
    historial.sort(key=lambda x: x["fecha_entrada"], reverse=True)
    return historial