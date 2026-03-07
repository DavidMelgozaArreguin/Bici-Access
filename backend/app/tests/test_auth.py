import pytest

# ============ TESTS DE LOGIN ============

def test_login_success(test_client):
    """
    Test: Login con credenciales correctas debe devolver token.
    """
    login_data = {
        "email": "david.melgoza@alumnos.udg.mx",
        "password": "secret"
    }
    
    response = test_client.post("/auth/login", json=login_data)
    
    # Verificar que la respuesta es exitosa
    assert response.status_code == 200
    
    # Verificar que contiene el token
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    
    # Verificar que el token no está vacío
    assert len(data["access_token"]) > 10

def test_login_wrong_password(test_client):
    """
    Test: Login con contraseña incorrecta debe fallar.
    """
    login_data = {
        "email": "david.melgoza@alumnos.udg.mx",
        "password": "contrasena_equivocada"
    }
    
    response = test_client.post("/auth/login", json=login_data)
    
    # Debe fallar con 401 Unauthorized
    assert response.status_code == 401
    
    # El mensaje de error debe ser claro
    data = response.json()
    assert "detail" in data
    assert "credenciales" in data["detail"].lower()

def test_login_wrong_email(test_client):
    """
    Test: Login con email incorrecto debe fallar.
    """
    login_data = {
        "email": "email_que_no_existe@alumnos.udg.mx",
        "password": "secret"
    }
    
    response = test_client.post("/auth/login", json=login_data)
    
    # Debe fallar con 401 Unauthorized
    assert response.status_code == 401

def test_login_invalid_email_format(test_client):
    """
    Test: Login con formato de email inválido debe fallar.
    """
    login_data = {
        "email": "no_es_email_udg@gmail.com",  # No es @alumnos.udg.mx
        "password": "secret"
    }
    
    response = test_client.post("/auth/login", json=login_data)
    
    # FastAPI valida el formato con Pydantic, debe dar 422
    assert response.status_code == 422
    
    # Verificar que el error menciona el formato del email
    data = response.json()
    assert "detail" in data

# ============ TESTS DE ENDPOINTS PROTEGIDOS ============

def test_protected_endpoint_without_token(test_client):
    """
    Test: Acceder a endpoint protegido sin token debe dar 401.
    """
    response = test_client.get("/users/me")
    
    # Sin token debe dar 401 (o 403 dependiendo de la configuración)
    assert response.status_code == 401
    
    # Debe indicar que se requiere autenticación
    data = response.json()
    assert "detail" in data

def test_protected_endpoint_with_invalid_token(test_client):
    """
    Test: Acceder a endpoint protegido con token inválido debe dar 401.
    """
    headers = {
        "Authorization": "Bearer token_invalido_falso_12345"
    }
    
    response = test_client.get("/users/me", headers=headers)
    
    # Token inválido debe dar 401
    assert response.status_code == 401

def test_protected_endpoint_with_valid_token(test_client, valid_token):
    """
    Test: Acceder a endpoint protegido con token válido debe funcionar.
    """
    headers = {
        "Authorization": f"Bearer {valid_token}"
    }
    
    response = test_client.get("/users/me", headers=headers)
    
    # Con token válido debe funcionar
    assert response.status_code == 200
    
    # Debe devolver los datos del usuario
    data = response.json()
    assert "email" in data
    assert "nombre" in data
    assert "codigo" in data

# ============ TESTS DE RATE LIMITING ============

def test_rate_limiting(test_client):
    """
    Test: El rate limiting funciona (máximo 5 intentos por minuto).
    """
    login_data = {
        "email": "david.melgoza@alumnos.udg.mx",
        "password": "contrasena_equivocada"
    }
    
    # Intentamos 6 veces (el límite es 5 por minuto)
    responses = []
    for i in range(6):
        response = test_client.post("/auth/login", json=login_data)
        responses.append(response.status_code)
    
    # Las primeras 5 deben ser 401, la 6ta debe ser 429 (Too Many Requests)
    assert 429 in responses  # Debe haber al menos un 429
    assert responses[-1] == 429  # El último intento debe ser bloqueado
    
    # Verificar que el error de rate limiting tiene el mensaje correcto
    last_response = test_client.post("/auth/login", json=login_data)
    assert last_response.status_code == 429
    data = last_response.json()
    assert "detail" in data