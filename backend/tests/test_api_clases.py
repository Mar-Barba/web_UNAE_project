import pytest
from unittest.mock import patch, MagicMock

# --- TESTS PARA CLASES ---
@patch("database.connection.get_db_connection")
def test_get_clases_exitoso(mock_get_conn, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_get_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    # Simulamos el retorno de la DB
    mock_cur.fetchall.return_value = [{"group": "A"}, {"group": "B"}]
    
    response = client.get("/api/clases")
    assert response.status_code == 200
    assert response.json["status"] == "successful"
    assert len(response.json["clases"]) == 2

@patch("database.connection.get_db_connection")
def test_get_clases_sin_conexion(mock_get_conn, client):
    mock_get_conn.return_value = None
    response = client.get("/api/clases")
    assert response.status_code == 500
    assert response.json["status"] == "error"

@patch("database.connection.get_db_connection")
def test_get_clases_excepcion(mock_get_conn, client):
    mock_get_conn.side_effect = Exception("DB Down")
    response = client.get("/api/clases")
    assert response.status_code == 500

@patch("database.clases.db_insert_clase")
def test_crear_clase_exitoso(mock_insert, client):
    mock_insert.return_value = True
    response = client.post("/api/clases", json={"username": "test", "maestro_id": "123"})
    assert response.status_code == 200
    assert response.json["status"] == "exitoso"

def test_crear_clase_faltan_datos(client):
    response = client.post("/api/clases", json={"username": "test"})
    assert response.status_code == 400
    assert response.json["status"] == "fail"

@patch("database.clases.db_insert_clase")
def test_crear_clase_falla_db(mock_insert, client):
    mock_insert.return_value = None
    response = client.post("/api/clases", json={"username": "test", "maestro_id": "123"})
    assert response.status_code == 500
    assert response.json["status"] == "fail"

@patch("database.clases.db_insert_clase")
def test_crear_clase_excepcion(mock_insert, client):
    mock_insert.side_effect = Exception("DB Error")
    response = client.post("/api/clases", json={"username": "test", "maestro_id": "123"})
    assert response.status_code == 400

@patch("database.connection.get_db_connection")
def test_get_metrics_clase_exitoso(mock_get_conn, client):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_get_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cur
    
    mock_cur.fetchall.return_value = [
        {"time_played": 100, "score": 50, "username": "user1", "id": 1}
    ]
    
    response = client.get("/api/metrics/clase/A")
    assert response.status_code == 200
    assert response.json["status"] == "successful"
    assert response.json["data"]["alumnos"][0] == "user1"

@patch("database.connection.get_db_connection")
def test_get_metrics_clase_excepcion(mock_get_conn, client):
    mock_get_conn.side_effect = Exception("Error")
    response = client.get("/api/metrics/clase/A")
    assert response.status_code == 400
