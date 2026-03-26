from fastapi import APIRouter, Depends, HTTPException, Request
from uuid import uuid4

from app.logger import log_bicicleta_event
from app.models import BicicletaCreate, BicicletaOut, UserOut
from app.dependencies import get_current_user
from app.database.bicis import bicis_collection
from datetime import datetime, timezone

router = APIRouter(prefix="/bicicletas", tags=["bicicletas"])


@router.post("/", response_model=BicicletaOut)
async def registrar_bicicleta(
    bicicleta: BicicletaCreate,
    current_user: UserOut = Depends(get_current_user),
    request: Request = None
):
    bici_existente = bicis_collection.find_one({"serial": bicicleta.serial})
    if bici_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una bicicleta con este número de serie."
        )

    new_id = str(uuid4())[:8]

    nueva_bicicleta = {
        "id": str(uuid4())[:8],
        "propietario_id": current_user.id,
        "marca": bicicleta.marca,
        "modelo": bicicleta.modelo,
        "color": bicicleta.color,
        "serial": bicicleta.serial,
        "fecha_registro": datetime.now(timezone.utc)
    }

    bicis_collection.insert_one(nueva_bicicleta)

    if request:
        client_ip = request.client.host if request.client else "unknown"
        log_bicicleta_event("registro", new_id, current_user.id, client_ip)

    return nueva_bicicleta


@router.get("/mis-bicicletas", response_model=list[BicicletaOut])
async def listar_mis_bicicletas(
    current_user: UserOut = Depends(get_current_user)
):
    bicicletas = list(
        bicis_collection.find(
            {"propietario_id": current_user.id},
            {"_id": 0}
        )
    )
    return bicicletas


@router.get("/{bici_id}", response_model=BicicletaOut)
async def obtener_bicicleta(
    bici_id: str,
    current_user: UserOut = Depends(get_current_user)
):
    bici = bicis_collection.find_one({"id": bici_id}, {"_id": 0})

    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")

    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para acceder a esta bicicleta"
        )

    return bici


@router.put("/{bici_id}", response_model=BicicletaOut)
async def actualizar_bicicleta(
    bici_id: str,
    bici_actualizada: BicicletaCreate,
    current_user: UserOut = Depends(get_current_user),
    request: Request = None
):
    bici = bicis_collection.find_one({"id": bici_id})

    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")

    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para modificar esta bicicleta"
        )

    serial_existente = bicis_collection.find_one({"serial": bici_actualizada.serial})
    if serial_existente and serial_existente["id"] != bici_id:
        raise HTTPException(
            status_code=400,
            detail="Ya existe otra bicicleta con este número de serie"
        )

    bicis_collection.update_one(
        {"id": bici_id},
        {"$set": {
            "marca": bici_actualizada.marca,
            "modelo": bici_actualizada.modelo,
            "color": bici_actualizada.color,
            "serial": bici_actualizada.serial
        }}
    )

    bici_actualizada_db = bicis_collection.find_one({"id": bici_id}, {"_id": 0})

    if request:
        client_ip = request.client.host if request.client else "unknown"
        log_bicicleta_event("actualizacion", bici_id, current_user.id, client_ip)

    return bici_actualizada_db

 
@router.delete("/{bici_id}")
async def eliminar_bicicleta(
    bici_id: str,
    current_user: UserOut = Depends(get_current_user),
    request: Request = None
):
    bici = bicis_collection.find_one({"id": bici_id})

    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")

    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para eliminar esta bicicleta"
        )

    bicis_collection.delete_one({"id": bici_id})

    if request:
        client_ip = request.client.host if request.client else "unknown"
        log_bicicleta_event("eliminacion", bici_id, current_user.id, client_ip)

    return {"message": "Bicicleta eliminada correctamente"}