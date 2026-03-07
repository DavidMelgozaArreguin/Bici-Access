import pytest

# ============ TESTS DE BICICLETAS ============

def test_register_bicycle_without_auth(test_client):
    """
    Test: Intentar registrar bicicleta sin estar autenticado debe fallar.
    """
    bike_data = {
        "marca": "Test Bike",
        "modelo": "Model X",
        "color": "Azul",
        "serial": "TEST12345"
    }
    
    response = test_client.post("/bicicletas/", json=bike_data)
    
    # Debe fallar con 401 (no autenticado)
    assert response.status_code == 401

def test_register_bicycle_with_auth(test_client, valid_token):
    """
    Test: Registrar bicicleta con autenticación debe funcionar.
    """
    headers = {
        "Authorization": f"Bearer {valid_token}"
    }
    
    bike_data = {
        "marca": "Test Bike",
        "modelo": "Model X",
        "color": "Azul",
        "serial": "TEST99999"  # Serial único para cada test
    }
    
    response = test_client.post("/bicicletas/", json=bike_data, headers=headers)
    
    # Debe funcionar con token válido
    assert response.status_code == 200
    
    # Debe devolver los datos de la bicicleta
    data = response.json()
    assert data["marca"] == "Test Bike"
    assert data["modelo"] == "Model X"
    assert data["color"] == "Azul"
    assert data["serial"] == "TEST99999"
    assert "id" in data
    assert "propietario_id" in data

def test_list_bicycles_with_auth(test_client, valid_token):
    """
    Test: Listar bicicletas con autenticación debe funcionar.
    """
    headers = {
        "Authorization": f"Bearer {valid_token}"
    }
    
    response = test_client.get("/bicicletas/mis-bicicletas", headers=headers)
    
    # Debe funcionar con token válido
    assert response.status_code == 200
    
    # Debe devolver una lista (puede estar vacía)
    data = response.json()
    assert isinstance(data, list)