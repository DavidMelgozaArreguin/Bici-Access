import pytest
from fastapi.testclient import TestClient
from app.main import app
import sys
import os

# Añadir el directorio 'app' al path para las importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Este fixture crea un cliente de test para cada test
@pytest.fixture(scope="module")
def test_client():
    """
    Crea un cliente de prueba para la app FastAPI.
    Este cliente se reutiliza en todos los tests del módulo.
    """
    with TestClient(app) as client:
        yield client

# Fixture para obtener un token válido (para tests que lo necesiten)
@pytest.fixture(scope="module")
def valid_token(test_client):
    """
    Obtiene un token JWT válido para usar en tests.
    """
    login_data = {
        "email": "david.melgoza@alumnos.udg.mx",
        "password": "secret"
    }
    response = test_client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]