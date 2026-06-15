import pytest
from unittest.mock import patch

# --- TESTS PARA PUT /api/users ---
@patch("main.db_update_user")
def test_update_usuario_exitoso(mock_update, client):
    mock_update.return_value = True
    response = client.put("/api/users/1", json={"parameter": "rol", "value": "admin"})
    assert response.status_code == 200
    assert response.json["status"] == "successful"

@patch("main.db_update_user")
def test_update_usuario_falla_db(mock_update, client):
    mock_update.return_value = None
    response = client.put("/api/users/1", json={"parameter": "rol", "value": "admin"})
    assert response.status_code == 500

@patch("main.db_update_user")
def test_update_usuario_excepcion(mock_update, client):
    mock_update.side_effect = Exception("Error")
    response = client.put("/api/users/1", json={})
    assert response.status_code == 400

# --- TESTS PARA LOGIN ---
@patch("main.check_password_hash")
@patch("main.db_read_user")
def test_validar_usuario_exitoso(mock_read, mock_check, client):
    mock_read.return_value = [{"id": 1, "password": "hashed", "rol": "student"}]
    mock_check.return_value = True
    response = client.post("/api/users/login", json={"username": "test", "password": "123"})
    assert response.status_code == 200
    assert response.json["valido"] is True

@patch("main.db_read_user")
def test_validar_usuario_no_encontrado(mock_read, client):
    mock_read.return_value = []
    response = client.post("/api/users/login", json={"username": "test"})
    assert response.status_code == 404

@patch("main.check_password_hash")
@patch("main.db_read_user")
def test_validar_usuario_pass_invalida(mock_read, mock_check, client):
    mock_read.return_value = [{"id": 1, "password": "hashed", "rol": "student"}]
    mock_check.return_value = False
    response = client.post("/api/users/login", json={"username": "test", "password": "bad"})
    assert response.status_code == 401

@patch("main.db_read_user")
def test_validar_usuario_excepcion(mock_read, client):
    mock_read.side_effect = Exception("Error")
    response = client.post("/api/users/login", json={"username": "test"})
    assert response.status_code == 401

# --- TESTS PARA METRICS INDIVIDUAL ---
@patch("main.db_get_player_full_metrics")
def test_get_metrics_individual_exitoso(mock_metrics, client):
    mock_metrics.return_value = {
        "resumen": {"tiempo_total_segundos": 125},
        "sesiones": [{"tiempo": 65}, {"tiempo": None}]
    }
    response = client.get("/api/metrics/player/user1")
    assert response.status_code == 200
    assert response.json["resumen"]["tiempo_total"] == "02:05"
    assert response.json["sesiones"][0]["tiempo"] == "01:05"
    assert response.json["sesiones"][1]["tiempo"] == "00:00"

@patch("main.db_get_player_full_metrics")
def test_get_metrics_individual_no_encontrado(mock_metrics, client):
    mock_metrics.return_value = None
    response = client.get("/api/metrics/player/user1")
    assert response.status_code == 404

# --- TESTS PARA METRICS RECENT ---
@patch("main.db_get_all_recent_sessions")
def test_get_metrics_recent_exitoso(mock_recent, client):
    mock_recent.return_value = [{"id": 1}]
    response = client.get("/api/metrics/recent")
    assert response.status_code == 200

@patch("main.db_get_all_recent_sessions")
def test_get_metrics_recent_error(mock_recent, client):
    mock_recent.return_value = None
    response = client.get("/api/metrics/recent")
    assert response.status_code == 500

# --- TESTS PARA ACHIEVEMENTS ---
@patch("main.db_insert_achievement")
def test_create_achievement(mock_insert, client):
    mock_insert.return_value = True
    response = client.post("/api/achievements", json={"name": "A"})
    assert response.status_code == 200

    mock_insert.return_value = None
    response = client.post("/api/achievements", json={})
    assert response.status_code == 500

    mock_insert.side_effect = Exception("Error")
    response = client.post("/api/achievements", json={})
    assert response.status_code == 400

@patch("main.db_read_achievement")
def test_get_achievement(mock_read, client):
    mock_read.return_value = {"id": 1}
    response = client.get("/api/achievements/1")
    assert response.status_code == 200

    mock_read.return_value = None
    response = client.get("/api/achievements/1")
    assert response.status_code == 404

    mock_read.side_effect = Exception("Error")
    response = client.get("/api/achievements/1")
    assert response.status_code == 400

@patch("main.db_update_achievement")
def test_update_achievement(mock_update, client):
    mock_update.return_value = True
    response = client.put("/api/achievements/1", json={})
    assert response.status_code == 200

    mock_update.return_value = None
    response = client.put("/api/achievements/1", json={})
    assert response.status_code == 500

    mock_update.side_effect = Exception("Error")
    response = client.put("/api/achievements/1", json={})
    assert response.status_code == 400

@patch("main.db_delete_achievement")
def test_delete_achievement(mock_delete, client):
    mock_delete.return_value = True
    response = client.delete("/api/achievements", json={"achievement_id": 1})
    assert response.status_code == 200

    mock_delete.return_value = None
    response = client.delete("/api/achievements", json={})
    assert response.status_code == 500

    mock_delete.side_effect = Exception("Error")
    response = client.delete("/api/achievements", json={})
    assert response.status_code == 400

# --- TESTS PARA LEVELS ---
@patch("main.db_insert_level")
def test_create_level(mock_insert, client):
    mock_insert.return_value = True
    response = client.post("/api/levels", json={"level_num": 1})
    assert response.status_code == 200

    mock_insert.return_value = None
    response = client.post("/api/levels", json={})
    assert response.status_code == 500

    mock_insert.side_effect = Exception("Error")
    response = client.post("/api/levels", json={})
    assert response.status_code == 400

@patch("main.db_read_level")
def test_get_level(mock_read, client):
    mock_read.return_value = {"id": 1}
    response = client.get("/api/levels/1")
    assert response.status_code == 200

    mock_read.return_value = None
    response = client.get("/api/levels/1")
    assert response.status_code == 404

    mock_read.side_effect = Exception("Error")
    response = client.get("/api/levels/1")
    assert response.status_code == 400

@patch("main.db_update_level")
def test_update_level(mock_update, client):
    mock_update.return_value = True
    response = client.put("/api/levels/1", json={})
    assert response.status_code == 200

    mock_update.return_value = None
    response = client.put("/api/levels/1", json={})
    assert response.status_code == 500

    mock_update.side_effect = Exception("Error")
    response = client.put("/api/levels/1", json={})
    assert response.status_code == 400

@patch("main.db_delete_level")
def test_delete_level(mock_delete, client):
    mock_delete.return_value = True
    response = client.delete("/api/levels", json={"level_id": 1})
    assert response.status_code == 200

    mock_delete.return_value = None
    response = client.delete("/api/levels", json={})
    assert response.status_code == 500

    mock_delete.side_effect = Exception("Error")
    response = client.delete("/api/levels", json={})
    assert response.status_code == 400

# --- TESTS PARA GAME SESSIONS ---
@patch("main.db_insert_game_session")
def test_create_session(mock_insert, client):
    mock_insert.return_value = True
    response = client.post("/api/sessions", json={"user_id": 1})
    assert response.status_code == 200

    mock_insert.return_value = None
    response = client.post("/api/sessions", json={})
    assert response.status_code == 500

    mock_insert.side_effect = Exception("Error")
    response = client.post("/api/sessions", json={})
    assert response.status_code == 400

@patch("main.db_read_game_session")
def test_get_session(mock_read, client):
    mock_read.return_value = {"id": 1}
    response = client.get("/api/sessions/1")
    assert response.status_code == 200

    mock_read.return_value = None
    response = client.get("/api/sessions/1")
    assert response.status_code == 404

    mock_read.side_effect = Exception("Error")
    response = client.get("/api/sessions/1")
    assert response.status_code == 400

@patch("main.db_update_game_session")
def test_update_session(mock_update, client):
    mock_update.return_value = True
    response = client.put("/api/sessions/1", json={})
    assert response.status_code == 200

    mock_update.return_value = None
    response = client.put("/api/sessions/1", json={})
    assert response.status_code == 500

    mock_update.side_effect = Exception("Error")
    response = client.put("/api/sessions/1", json={})
    assert response.status_code == 400

@patch("main.db_delete_game_session")
def test_delete_session(mock_delete, client):
    mock_delete.return_value = True
    response = client.delete("/api/sessions", json={"session_id": 1})
    assert response.status_code == 200

    mock_delete.return_value = None
    response = client.delete("/api/sessions", json={})
    assert response.status_code == 500

    mock_delete.side_effect = Exception("Error")
    response = client.delete("/api/sessions", json={})
    assert response.status_code == 400

# --- TESTS PARA USER ACHIEVEMENTS ---
@patch("main.db_insert_user_achievement")
def test_create_user_achievement(mock_insert, client):
    mock_insert.return_value = True
    response = client.post("/api/user_achievements", json={"user_id": 1})
    assert response.status_code == 200

    mock_insert.return_value = None
    response = client.post("/api/user_achievements", json={})
    assert response.status_code == 500

    mock_insert.side_effect = Exception("Error")
    response = client.post("/api/user_achievements", json={})
    assert response.status_code == 400

@patch("main.db_read_user_achievement")
def test_get_user_achievement(mock_read, client):
    mock_read.return_value = {"id": 1}
    response = client.get("/api/user_achievements/1/1")
    assert response.status_code == 200

    mock_read.return_value = None
    response = client.get("/api/user_achievements/1/1")
    assert response.status_code == 404

    mock_read.side_effect = Exception("Error")
    response = client.get("/api/user_achievements/1/1")
    assert response.status_code == 400

@patch("main.db_update_user_achievement")
def test_update_user_achievement(mock_update, client):
    mock_update.return_value = True
    response = client.put("/api/user_achievements/1/1", json={})
    assert response.status_code == 200

    mock_update.return_value = None
    response = client.put("/api/user_achievements/1/1", json={})
    assert response.status_code == 500

    mock_update.side_effect = Exception("Error")
    response = client.put("/api/user_achievements/1/1", json={})
    assert response.status_code == 400

@patch("main.db_delete_user_achievement")
def test_delete_user_achievement(mock_delete, client):
    mock_delete.return_value = True
    response = client.delete("/api/user_achievements", json={"user_id": 1, "achievement_id": 1})
    assert response.status_code == 200

    mock_delete.return_value = None
    response = client.delete("/api/user_achievements", json={})
    assert response.status_code == 500

    mock_delete.side_effect = Exception("Error")
    response = client.delete("/api/user_achievements", json={})
    assert response.status_code == 400

# --- TESTS PARA OTRAS RUTAS ---
@patch("main.send_from_directory")
def test_api_files(mock_send, client):
    mock_send.return_value = "file_content"
    response = client.get("/api/api/test.txt")
    assert response.status_code == 200
    assert response.data == b"file_content"

def test_index(client):
    response = client.get("/api/")
    assert response.status_code == 200
    assert b"Dashboard Memoretos" in response.data
