from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import StreamingResponse
from app.models import BicicletaCreate, BicicletaOut, UserOut
from app.dependencies import get_current_user
from app.database import (
    get_bicicleta_by_id, get_bicicletas_by_usuario,
    create_bicicleta, update_bicicleta, delete_bicicleta,
    get_user_by_id, fake_bicicletas_db
)
from app.logger import log_bicicleta_event
import qrcode
import io
import uuid

router = APIRouter(prefix="/bicicletas", tags=["bicicletas"])

# ============ CREATE ============

@router.post("/", response_model=BicicletaOut)
async def registrar_bicicleta(
    request: Request,
    bicicleta: BicicletaCreate,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Registra una nueva bicicleta para el usuario actual.
    """
    # Verificar si el serial ya existe (en toda la BD)
    for bici in fake_bicicletas_db.values():
        if bici["serial"] == bicicleta.serial:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una bicicleta con este número de serie"
            )
    
    # Crear bicicleta
    bici_data = bicicleta.dict()
    bici_data["propietario_id"] = current_user.id
    
    nueva_bici = create_bicicleta(bici_data)
    
    # Log
    log_bicicleta_event("registro", nueva_bici["id"], current_user.id, request.client.host)
    
    return nueva_bici

# ============ READ (listar mis bicis) ============

@router.get("/mis-bicicletas", response_model=list[BicicletaOut])
async def listar_mis_bicicletas(
    request: Request,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Devuelve todas las bicicletas del usuario actual.
    """
    bicis = get_bicicletas_by_usuario(current_user.id)
    return bicis

# ============ READ (una bici específica) ============

@router.get("/{bici_id}", response_model=BicicletaOut)
async def obtener_bicicleta(
    request: Request,
    bici_id: str,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Obtiene los detalles de una bicicleta específica.
    """
    bici = get_bicicleta_by_id(bici_id)
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")
    
    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para acceder a esta bicicleta"
        )
    
    return bici

# ============ QR ============

@router.get("/{bici_id}/qr")
async def generar_qr_bicicleta(
    request: Request,
    bici_id: str,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Genera un código QR para la bicicleta.
    El QR contiene un identificador único que puede ser escaneado para entrada/salida.
    """
    bici = get_bicicleta_by_id(bici_id)
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")
    
    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para generar QR de esta bicicleta"
        )
    
    # Contenido del QR (puede ser una URL o un identificador)
    # Ejemplo: "ciclopuerto://bicicleta/bici_1"
    qr_content = f"ciclopuerto://bicicleta/{bici_id}"
    
    # Generar QR
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(qr_content)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar en buffer de memoria
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Devolver como imagen
    return StreamingResponse(
        img_buffer, 
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename=bicicleta_{bici_id}.png"}
    )

# ============ UPDATE ============

@router.put("/{bici_id}", response_model=BicicletaOut)
async def actualizar_bicicleta(
    request: Request,
    bici_id: str,
    bici_actualizada: BicicletaCreate,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Actualiza los datos de una bicicleta existente.
    """
    bici = get_bicicleta_by_id(bici_id)
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")
    
    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para modificar esta bicicleta"
        )
    
    # Verificar serial único (excepto si es el mismo)
    if bici_actualizada.serial != bici["serial"]:
        for otra in fake_bicicletas_db.values():
            if otra["serial"] == bici_actualizada.serial and otra["id"] != bici_id:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe otra bicicleta con este número de serie"
                )
    
    # Actualizar
    bici.update(bici_actualizada.dict())
    
    log_bicicleta_event("actualizacion", bici_id, current_user.id, request.client.host)
    
    return bici

# ============ DELETE ============

@router.delete("/{bici_id}")
async def eliminar_bicicleta(
    request: Request,
    bici_id: str,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Elimina (da de baja) una bicicleta.
    """
    bici = get_bicicleta_by_id(bici_id)
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")
    
    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para eliminar esta bicicleta"
        )
    
    delete_bicicleta(bici_id)
    
    log_bicicleta_event("eliminacion", bici_id, current_user.id, request.client.host)
    
    return {"message": "Bicicleta eliminada correctamente"}