from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models import UserOut
from app.dependencies import get_current_admin
from app.database import fake_users_db, fake_bicicletas_db, fake_registros_db

router = APIRouter(prefix="/admin", tags=["admin"])

# ENDPOINTS PARA USUARIOS

@router.get("/usuarios", response_model=List[UserOut])
async def obtener_todos_usuarios(
    admin: UserOut = Depends(get_current_admin)  # Solo admin puede acceder
):
    """
    Obtiene la lista de TODOS los usuarios registrados.
    Solo para administradores.
    """
    usuarios = []
    for user_id, user_data in fake_users_db.items():
        # Crear un UserOut para cada usuario
        usuario = UserOut(**user_data)
        usuarios.append(usuario)
    
    return usuarios

# ENDPOINTS PARA BICICLETAS 

@router.get("/bicicletas")
async def obtener_todas_bicicletas(
    admin: UserOut = Depends(get_current_admin)
):
    """
    Obtiene la lista de TODAS las bicicletas registradas.
    Solo para administradores.
    """
    # Convertimos el diccionario a lista
    todas_bicis = list(fake_bicicletas_db.values())
    
    # Para cada bici, añadimos el nombre del dueño
    for bici in todas_bicis:
        # Buscamos el usuario dueño
        for user_id, user_data in fake_users_db.items():
            if user_data["id"] == bici["propietario_id"]:
                bici["propietario_nombre"] = user_data["nombre"]
                bici["propietario_email"] = user_data["email"]
                break
    
    return todas_bicis

# ENDPOINTS PARA REGISTROS 

@router.get("/registros")
async def obtener_todos_registros(
    admin: UserOut = Depends(get_current_admin)
):
    """
    Obtiene TODOS los registros de entrada/salida.
    Solo para administradores.
    """
    todos_registros = list(fake_registros_db.values())
    
    # Ordenar por fecha de entrada (más reciente primero)
    todos_registros.sort(key=lambda x: x["fecha_entrada"], reverse=True)
    
    return todos_registros

# ESTADÍSTICAS PARA ADMIN 

@router.get("/estadisticas")
async def obtener_estadisticas(
    admin: UserOut = Depends(get_current_admin)
):
    """
    Estadísticas generales del sistema.
    Solo para administradores.
    """
    total_usuarios = len(fake_users_db)
    total_bicicletas = len(fake_bicicletas_db)
    total_registros = len(fake_registros_db)
    
    # Contar bicicletas actualmente dentro
    bicis_dentro = 0
    for reg in fake_registros_db.values():
        if reg["activo"]:
            bicis_dentro += 1
    
    # Contar por rol
    estudiantes = 0
    admins = 0
    for user in fake_users_db.values():
        if user["rol"] == "estudiante":
            estudiantes += 1
        elif user["rol"] == "admin":
            admins += 1
    
    return {
        "resumen": {
            "total_usuarios": total_usuarios,
            "total_bicicletas": total_bicicletas,
            "total_registros": total_registros,
            "bicicletas_actualmente_dentro": bicis_dentro
        },
        "desglose_roles": {
            "estudiantes": estudiantes,
            "administradores": admins
        }
    }