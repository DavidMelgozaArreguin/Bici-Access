import logging
import sys
from datetime import datetime
import json

# Configurar el logger principal
logger = logging.getLogger("ciclopuerto")
logger.setLevel(logging.INFO)

# Formato personalizado
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - IP:%(client_ip)s - %(message)s'
)

# Handler para consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Handler para archivo (rotativo)
from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler(
    'ciclopuerto.log', maxBytes=10485760, backupCount=5  # 10MB por archivo, 5 archivos de backup
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Funciones de ayuda para logging estructurado
def log_login_attempt(email: str, success: bool, client_ip: str, details: str = ""):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "event": "login_attempt",
        "email": email,
        "success": success,
        "client_ip": client_ip,
        "details": details
    }
    if success:
        logger.info(f"Login exitoso: {email}", extra={"client_ip": client_ip})
    else:
        logger.warning(f"Login fallido: {email} - {details}", extra={"client_ip": client_ip})

def log_bicicleta_event(event_type: str, bicicleta_id: str, usuario_id: int, client_ip: str):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "bicicleta_id": bicicleta_id,
        "usuario_id": usuario_id,
        "client_ip": client_ip
    }
    logger.info(f"Evento {event_type}: bici {bicicleta_id} por usuario {usuario_id}", 
                extra={"client_ip": client_ip})

def log_registro_event(event_type: str, registro_id: str, usuario_id: int, client_ip: str):
    logger.info(f"Registro {event_type}: ID {registro_id} por usuario {usuario_id}",
                extra={"client_ip": client_ip})