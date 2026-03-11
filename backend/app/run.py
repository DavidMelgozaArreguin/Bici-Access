"""
Script para probar la generación de QR.
Ejecutar: python run.py
"""

import requests
from io import BytesIO
from PIL import Image

# Primero hacer login para obtener token
login_data = {
    "email": "david.melgoza@alumnos.udg.mx",
    "password": "secret"
}
response = requests.post("http://localhost:8000/auth/login", json=login_data)
token = response.json()["access_token"]

# Obtener QR de una bicicleta (ej: bici_1)
headers = {"Authorization": f"Bearer {token}"}
qr_response = requests.get("http://localhost:8000/bicicletas/bici_1/qr", headers=headers)

if qr_response.status_code == 200:
    # Guardar imagen
    img = Image.open(BytesIO(qr_response.content))
    img.save("qr_bici_1.png")
    print("✅ QR guardado como qr_bici_1.png")
else:
    print("❌ Error:", qr_response.json())