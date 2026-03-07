from app.logger import log_bicicleta_event
from fastapi import APIRouter, Depends, HTTPException
from app.models import BicicletaCreate, BicicletaOut, UserOut
from app.dependencies import get_current_user
from app.database import fake_bicicletas_db
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Request  # <-- Añadir Request

router = APIRouter(prefix="/bicicletas", tags=["bicicletas"])

# CREATE
@router.post("/", response_model=BicicletaOut)
async def registrar_bicicleta(
    bicicleta: BicicletaCreate,
    current_user: UserOut = Depends(get_current_user),
    request: Request = None
):
    # Verificar si el serial ya existe
    for bici_id, bici_data in fake_bicicletas_db.items():
        if bici_data["serial"] == bicicleta.serial:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una bicicleta con este número de serie."
            )
    
    # Crear un nuevo ID para la bici
    new_id = str(uuid4())[:8]
    
    # Crear el diccionario de la bicicleta
    nueva_bicicleta = {
        "id": new_id,
        "propietario_id": current_user.id,
        "marca": bicicleta.marca,
        "modelo": bicicleta.modelo,
        "color": bicicleta.color,
        "serial": bicicleta.serial
    }
    
    # Guardar en la "base de datos"
    fake_bicicletas_db[new_id] = nueva_bicicleta
    if request:
        client_ip = request.client.host if request.client else "unknown"
        log_bicicleta_event("registro", new_id, current_user.id, client_ip)
    return nueva_bicicleta

# READ (Listar todas las bicicletas del usuario)
@router.get("/mis-bicicletas", response_model=list[BicicletaOut])
async def listar_mis_bicicletas(
    current_user: UserOut = Depends(get_current_user)
):
    """
    Devuelve la lista de todas las bicicletas registradas por el usuario actual.
    """
    mis_bicicletas = []
    for bici_id, bici_data in fake_bicicletas_db.items():
        if bici_data["propietario_id"] == current_user.id:
            mis_bicicletas.append(bici_data)
    
    return mis_bicicletas

# READ (Obtener una bicicleta específica)
@router.get("/{bici_id}", response_model=BicicletaOut)
async def obtener_bicicleta(
    bici_id: str,
    current_user: UserOut = Depends(get_current_user)
):
    """
    Obtiene los detalles de una bicicleta específica por su ID.
    Solo el propietario puede verla.
    """
    # Verificar si la bicicleta existe
    bici = fake_bicicletas_db.get(bici_id)
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")
    
    # Verificar que el usuario sea el propietario
    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para acceder a esta bicicleta"
        )
    
    return bici

# UPDATE (Actualizar una bicicleta)
@router.put("/{bici_id}", response_model=BicicletaOut)
async def actualizar_bicicleta(
    bici_id: str,
    bici_actualizada: BicicletaCreate,
    current_user: UserOut = Depends(get_current_user),
    request: Request = None
):
    """
    Actualiza los datos de una bicicleta existente.
    Solo el propietario puede actualizarla.
    """
    # Verificar si la bicicleta existe
    bici = fake_bicicletas_db.get(bici_id)
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")
    
    # Verificar que el usuario sea el propietario
    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para modificar esta bicicleta"
        )
    
    # Verificar que el nuevo serial no exista en otra bicicleta
    if bici_actualizada.serial != bici["serial"]:  # Solo si cambió el serial
        for bici_key, bici_data in fake_bicicletas_db.items():
            if bici_data["serial"] == bici_actualizada.serial and bici_key != bici_id:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe otra bicicleta con este número de serie"
                )
    
    # Actualizar los datos de la bicicleta
    bici["marca"] = bici_actualizada.marca
    bici["modelo"] = bici_actualizada.modelo
    bici["color"] = bici_actualizada.color
    bici["serial"] = bici_actualizada.serial
    
    if request:
        client_ip = request.client.host if request.client else "unknown"
        log_bicicleta_event("actualizacion", bici_id, current_user.id, client_ip)


    return bici

# DELETE (Eliminar una bicicleta)
@router.delete("/{bici_id}")
async def eliminar_bicicleta(
    bici_id: str,
    current_user: UserOut = Depends(get_current_user),
    request: Request = None
):
    """
    Elimina una bicicleta del sistema (dar de baja).
    Solo el propietario puede eliminarla.
    """
    # Verificar si la bicicleta existe
    bici = fake_bicicletas_db.get(bici_id)
    if not bici:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")
    
    # Verificar que el usuario sea el propietario
    if bici["propietario_id"] != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para eliminar esta bicicleta"
        )
    
    # Eliminar la bicicleta
    del fake_bicicletas_db[bici_id]
    
    if request:
        client_ip = request.client.host if request.client else "unknown"
        log_bicicleta_event("eliminacion", bici_id, current_user.id, client_ip)

    return {"message": "Bicicleta eliminada correctamente"}