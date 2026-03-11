"""
Capa de abstracción de base de datos.
Por ahora usa datos falsos, pero está preparada para conectar a MongoDB real.
Cuando la BD esté lista, solo cambiarás las funciones internas.
"""

from datetime import datetime
from passlib.context import CryptContext
import uuid

# Configuración de hashing (igual que antes)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============ DATOS DE PRUEBA ============

# Usuarios de prueba
fake_users_db = {
    "2213522292": {
        "id": 1,
        "codigo": "2213522292",
        "nombre": "David Melgoza",
        "email": "david.melgoza@alumnos.udg.mx",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "rol": "admin",
        "fecha_registro": datetime.now()
    },
    "218555352": {
        "id": 2,
        "codigo": "218555352",
        "nombre": "Samuel Chavez",
        "email": "samuel.chavez@alumnos.udg.mx",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "rol": "estudiante",
        "fecha_registro": datetime.now()
    },
    "217034545": {
        "id": 3,
        "codigo": "217034545",
        "nombre": "Alan Valle",
        "email": "alan.valle@alumnos.udg.mx",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "rol": "estudiante",
        "fecha_registro": datetime.now()
    }
}

# Bicicletas de prueba
fake_bicicletas_db = {
    "bici_1": {
        "id": "bici_1",
        "propietario_id": 1,
        "marca": "Trek",
        "modelo": "Marlin 5",
        "color": "Rojo",
        "serial": "TRK123456",
        "fecha_registro": datetime.now(),
        "activa": True
    },
    "bici_2": {
        "id": "bici_2",
        "propietario_id": 1,
        "marca": "Specialized",
        "modelo": "Rockhopper",
        "color": "Azul",
        "serial": "SPC789012",
        "fecha_registro": datetime.now(),
        "activa": True
    },
    "bici_3": {
        "id": "bici_3",
        "propietario_id": 2,
        "marca": "Giant",
        "modelo": "Talon",
        "color": "Negro",
        "serial": "GNT345678",
        "fecha_registro": datetime.now(),
        "activa": True
    }
}

# Registros de prueba
fake_registros_db = {
    "reg_1": {
        "id": "reg_1",
        "bicicleta_id": "bici_1",
        "usuario_id": 1,
        "usuario_nombre": "David Melgoza",
        "bicicleta_marca": "Trek",
        "bicicleta_modelo": "Marlin 5",
        "fecha_entrada": datetime.now().replace(hour=8, minute=30),
        "fecha_salida": datetime.now().replace(hour=14, minute=45),
        "activo": False
    },
    "reg_2": {
        "id": "reg_2",
        "bicicleta_id": "bici_1",
        "usuario_id": 1,
        "usuario_nombre": "David Melgoza",
        "bicicleta_marca": "Trek",
        "bicicleta_modelo": "Marlin 5",
        "fecha_entrada": datetime.now().replace(hour=9, minute=15),
        "fecha_salida": None,
        "activo": True
    },
    "reg_3": {
        "id": "reg_3",
        "bicicleta_id": "bici_3",
        "usuario_id": 2,
        "usuario_nombre": "Samuel Chavez",
        "bicicleta_marca": "Giant",
        "bicicleta_modelo": "Talon",
        "fecha_entrada": datetime.now().replace(hour=10, minute=0),
        "fecha_salida": None,
        "activo": True
    }
}

# ============ FUNCIONES DE ACCESO A DATOS ============
# (Preparadas para migrar a MongoDB después)

# --- USUARIOS ---
def get_all_users():
    return list(fake_users_db.values())

def get_user_by_id(user_id):
    for user in fake_users_db.values():
        if user["id"] == user_id:
            return user
    return None

def get_user_by_email(email):
    for user in fake_users_db.values():
        if user["email"] == email:
            return user
    return None

def get_user_by_codigo(codigo):
    return fake_users_db.get(codigo)

def create_user(user_data):
    # Generar nuevo ID (el mayor + 1)
    new_id = max([u["id"] for u in fake_users_db.values()] + [0]) + 1
    user_data["id"] = new_id
    user_data["fecha_registro"] = datetime.now()
    user_data["rol"] = "estudiante"  # Por defecto
    fake_users_db[user_data["codigo"]] = user_data
    return user_data

# --- BICICLETAS ---
def get_all_bicicletas():
    return list(fake_bicicletas_db.values())

def get_bicicleta_by_id(bici_id):
    return fake_bicicletas_db.get(bici_id)

def get_bicicletas_by_usuario(usuario_id):
    return [b for b in fake_bicicletas_db.values() if b["propietario_id"] == usuario_id]

def create_bicicleta(bici_data):
    new_id = f"bici_{str(uuid.uuid4())[:8]}"
    bici_data["id"] = new_id
    bici_data["fecha_registro"] = datetime.now()
    bici_data["activa"] = True
    fake_bicicletas_db[new_id] = bici_data
    return bici_data

def update_bicicleta(bici_id, bici_data):
    if bici_id in fake_bicicletas_db:
        fake_bicicletas_db[bici_id].update(bici_data)
        return fake_bicicletas_db[bici_id]
    return None

def delete_bicicleta(bici_id):
    if bici_id in fake_bicicletas_db:
        del fake_bicicletas_db[bici_id]
        return True
    return False

# --- REGISTROS ---
def get_all_registros():
    return list(fake_registros_db.values())

def get_registros_by_usuario(usuario_id):
    return [r for r in fake_registros_db.values() if r["usuario_id"] == usuario_id]

def get_registros_activos_by_usuario(usuario_id):
    return [r for r in fake_registros_db.values() if r["usuario_id"] == usuario_id and r["activo"]]

def get_registro_activo_by_bicicleta(bicicleta_id):
    for r in fake_registros_db.values():
        if r["bicicleta_id"] == bicicleta_id and r["activo"]:
            return r
    return None

def create_registro_entrada(registro_data):
    new_id = f"reg_{str(uuid.uuid4())[:8]}"
    registro_data["id"] = new_id
    registro_data["fecha_entrada"] = datetime.now()
    registro_data["fecha_salida"] = None
    registro_data["activo"] = True
    fake_registros_db[new_id] = registro_data
    return registro_data

def update_registro_salida(registro_id):
    if registro_id in fake_registros_db:
        fake_registros_db[registro_id]["fecha_salida"] = datetime.now()
        fake_registros_db[registro_id]["activo"] = False
        return fake_registros_db[registro_id]
    return None