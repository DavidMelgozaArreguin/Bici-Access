from datetime import datetime, timedelta
import secrets

# Configuración para JWT. Cadena secreta y segura en producción
SECRET_KEY = "ciclopuerto_2v_secret_key_2025B" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # El token expira en 30 minutos


# Fake database para bicicletas
fake_users_db = {
    "2213522292": {
        "id": 1,
        "codigo": "2213522292",
        "nombre": "David Melgoza",
        "email": "david.melgoza@alumnos.udg.mx",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "rol": "admin"  # <--- NUEVO CAMPO AQUÍ
    },
    "218555352": {
        "id": 2,
        "codigo": "218555352",
        "nombre": "Samuel Chavez",
        "email": "samuel.chavez@alumnos.udg.mx",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "rol": "estudiante"  # <--- NUEVO CAMPO AQUÍ
    },
    "217034545": {  # Si Alan tiene un usuario
        "id": 3,
        "codigo": "217034545",
        "nombre": "Alan Valle",
        "email": "alan.valle@alumnos.udg.mx",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "rol": "estudiante"  # <--- NUEVO CAMPO AQUÍ
    }
}


fake_bicicletas_db = {}

#encriptado en bcrypt, base de datos falsa/temporal para ver si jala

ROLES = {
    "estudiante": "estudiante",
    "admin": "administrador",
    "vigilante": "vigilante"  # Por si luego agregas este rol
}
