import pytest
from unittest.mock import patch

@patch("main.db_insert_user")
def test_registrar_usuario_exitoso(mock_insert, client):
    mock_insert.return_value = {"id": 1} 
    response = client.post("/api/users", json={
        "username": "testuser",
        "mail": "test@test.com",
        "password": "password123",
        "rol": "student",
        "group": "A"
    })
    assert response.status_code == 200
    assert response.json["status"] == "exitoso"

@patch("main.db_insert_user")
def test_registrar_usuario_falla_db(mock_insert, client):
    mock_insert.return_value = None # Falla en base de datos
    response = client.post("/api/users", json={
        "username": "testuser"
    })
    assert response.status_code == 500
    assert response.json["status"] == "fail"

@patch("main.db_insert_user")
def test_registrar_usuario_excepcion(mock_insert, client):
    mock_insert.side_effect = Exception("DB Error") 
    response = client.post("/api/users", json={"username": "testuser"})
    assert response.status_code == 400
    assert response.json["status"] == "error"

@patch("main.db_delete_user")
def test_delete_usuario_exitoso(mock_delete, client):
    mock_delete.return_value = True
    response = client.delete("/api/users", json={"user_id": 1})
    assert response.status_code == 200

@patch("main.db_delete_user")
def test_delete_usuario_falla_db(mock_delete, client):
    mock_delete.return_value = None
    response = client.delete("/api/users", json={"user_id": 1})
    assert response.status_code == 500

@patch("main.db_delete_user")
def test_delete_usuario_excepcion(mock_delete, client):
    mock_delete.side_effect = Exception("Error")
    response = client.delete("/api/users", json={"user_id": 1})
    assert response.status_code == 400

# --- TESTS PARA GET /api/users/<id> ---
@patch("main.db_read_user_by_id")
def test_get_usuario_exitoso(mock_read, client):
    mock_read.return_value = {"id": 1, "username": "test"}
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json["user"]["username"] == "test"

@patch("main.db_read_user_by_id")
def test_get_usuario_no_encontrado(mock_read, client):
    mock_read.return_value = None
    response = client.get("/api/users/99")
    assert response.status_code == 404

@patch("main.db_read_user_by_id")
def test_get_usuario_excepcion(mock_read, client):
    mock_read.side_effect = Exception("Error")
    response = client.get("/api/users/1")
    assert response.status_code == 400