import pytest
from unittest.mock import MagicMock, patch
import psycopg2
import json
from flask import Flask
import importlib
import runpy

# Imports
from database.connection import get_db_connection
from database.achievements import db_insert_achievement, db_read_achievement, db_update_achievement, db_delete_achievement
from database.users import db_insert_user, db_delete_user, db_read_user, db_read_user_by_id, db_update_user
from database.game_sessions import db_insert_game_session, db_read_game_session, db_update_game_session, db_delete_game_session
from database.levels import db_insert_level, db_read_level, db_update_level, db_delete_level
from database.user_achievements import db_insert_user_achievement, db_read_user_achievement, db_update_user_achievement, db_delete_user_achievement
from database.metrics import db_get_player_full_metrics, db_get_all_recent_sessions

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def mock_conn():
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    return mock_conn, mock_cur

# --- Connection ---
def test_get_db_connection_success():
    with patch("psycopg2.connect") as mock_connect:
        mock_connect.return_value = MagicMock()
        conn = get_db_connection()
        assert conn is not None

def test_get_db_connection_fail():
    with patch("psycopg2.connect") as mock_connect:
        mock_connect.side_effect = Exception("Conn error")
        conn = get_db_connection()
        assert conn is None

# --- Achievements ---
def test_db_insert_achievement_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.achievements.get_db_connection", return_value=conn):
        assert db_insert_achievement("Name", "Desc", 10) is True
        conn.commit.assert_called_once()

def test_db_insert_achievement_fail_conn(app):
    with patch("database.achievements.get_db_connection", return_value=None):
        with app.app_context():
            res, code = db_insert_achievement("Name", "Desc", 10)
            assert code == 500

def test_db_insert_achievement_fail_sql(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = psycopg2.Error("SQL Error")
    with patch("database.achievements.get_db_connection", return_value=conn):
        assert db_insert_achievement("Name", "Desc", 10) is None
        conn.rollback.assert_called_once()

def test_db_insert_achievement_fail_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Random Error")
    with patch("database.achievements.get_db_connection", return_value=conn):
        assert db_insert_achievement("Name", "Desc", 10) is None
        conn.rollback.assert_called_once()

def test_db_read_achievement_success(mock_conn):
    conn, cur = mock_conn
    cur.fetchall.return_value = [{"id": 1}]
    with patch("database.achievements.get_db_connection", return_value=conn):
        assert db_read_achievement(1) == [{"id": 1}]

def test_db_read_achievement_fail_conn():
    with patch("database.achievements.get_db_connection", return_value=None):
        assert db_read_achievement(1) is None

def test_db_read_achievement_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.achievements.get_db_connection", return_value=conn):
        assert db_read_achievement(1) is None

def test_db_update_achievement_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.achievements.get_db_connection", return_value=conn):
        assert db_update_achievement(1, "name", "New") is True

def test_db_update_achievement_fail_conn():
    with patch("database.achievements.get_db_connection", return_value=None):
        assert db_update_achievement(1, "name", "New") is None

def test_db_update_achievement_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.achievements.get_db_connection", return_value=conn):
        assert db_update_achievement(1, "name", "New") is None
        conn.rollback.assert_called_once()

def test_db_delete_achievement_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.achievements.get_db_connection", return_value=conn):
        assert db_delete_achievement(1) is True

def test_db_delete_achievement_fail_conn():
    with patch("database.achievements.get_db_connection", return_value=None):
        assert db_delete_achievement(1) is None

def test_db_delete_achievement_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.achievements.get_db_connection", return_value=conn):
        assert db_delete_achievement(1) is None
        conn.rollback.assert_called_once()

# --- Users ---
def test_db_insert_user_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.users.get_db_connection", return_value=conn):
        assert db_insert_user("user", "mail", "pass", "rol") is True

def test_db_insert_user_fail_conn(app):
    with patch("database.users.get_db_connection", return_value=None):
        with app.app_context():
            res, code = db_insert_user("user", "mail", "pass", "rol")
            assert code == 500

def test_db_insert_user_fail_sql(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = psycopg2.Error("SQL Error")
    with patch("database.users.get_db_connection", return_value=conn):
        assert db_insert_user("user", "mail", "pass", "rol") is None

def test_db_insert_user_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.users.get_db_connection", return_value=conn):
        assert db_insert_user("user", "mail", "pass", "rol") is None

def test_db_delete_user_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.users.get_db_connection", return_value=conn):
        assert db_delete_user(1) is True

def test_db_delete_user_fail_conn():
    with patch("database.users.get_db_connection", return_value=None):
        assert db_delete_user(1) is None

def test_db_delete_user_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.users.get_db_connection", return_value=conn):
        assert db_delete_user(1) is None

def test_db_read_user_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.users.get_db_connection", return_value=conn):
        db_read_user("username")

def test_db_read_user_fail_conn():
    with patch("database.users.get_db_connection", return_value=None):
        assert db_read_user("username") is None

def test_db_read_user_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.users.get_db_connection", return_value=conn):
        assert db_read_user("username") is None

def test_db_read_user_by_id_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.users.get_db_connection", return_value=conn):
        db_read_user_by_id(1)

def test_db_read_user_by_id_fail_conn():
    with patch("database.users.get_db_connection", return_value=None):
        assert db_read_user_by_id(1) is None

def test_db_read_user_by_id_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.users.get_db_connection", return_value=conn):
        assert db_read_user_by_id(1) is None

def test_db_update_user_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.users.get_db_connection", return_value=conn):
        assert db_update_user(1, "username", "new") is True

def test_db_update_user_fail_conn():
    with patch("database.users.get_db_connection", return_value=None):
        assert db_update_user(1, "username", "new") is None

def test_db_update_user_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.users.get_db_connection", return_value=conn):
        assert db_update_user(1, "username", "new") is None

# --- Game Sessions ---
def test_db_insert_game_session_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.game_sessions.get_db_connection", return_value=conn):
        assert db_insert_game_session(1, 1, True, 100, 50, "2024-01-01") is True

def test_db_insert_game_session_fail_conn():
    with patch("database.game_sessions.get_db_connection", return_value=None):
        assert db_insert_game_session(1, 1, True, 100, 50, "2024-01-01") is None

def test_db_insert_game_session_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.game_sessions.get_db_connection", return_value=conn):
        assert db_insert_game_session(1, 1, True, 100, 50, "2024-01-01") is None

def test_db_read_game_session_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.game_sessions.get_db_connection", return_value=conn):
        db_read_game_session(1)

def test_db_read_game_session_fail_conn():
    with patch("database.game_sessions.get_db_connection", return_value=None):
        assert db_read_game_session(1) is None

def test_db_read_game_session_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.game_sessions.get_db_connection", return_value=conn):
        assert db_read_game_session(1) is None

def test_db_update_game_session_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.game_sessions.get_db_connection", return_value=conn):
        assert db_update_game_session(1, "score", 100) is True

def test_db_update_game_session_fail_conn():
    with patch("database.game_sessions.get_db_connection", return_value=None):
        assert db_update_game_session(1, "score", 100) is None

def test_db_update_game_session_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.game_sessions.get_db_connection", return_value=conn):
        assert db_update_game_session(1, "score", 100) is None

def test_db_delete_game_session_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.game_sessions.get_db_connection", return_value=conn):
        assert db_delete_game_session(1) is True

def test_db_delete_game_session_fail_conn():
    with patch("database.game_sessions.get_db_connection", return_value=None):
        assert db_delete_game_session(1) is None

def test_db_delete_game_session_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.game_sessions.get_db_connection", return_value=conn):
        assert db_delete_game_session(1) is None

# --- Levels ---
def test_db_insert_level_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.levels.get_db_connection", return_value=conn):
        assert db_insert_level(1, "Easy", {"config": 1}) is True

def test_db_insert_level_fail_conn():
    with patch("database.levels.get_db_connection", return_value=None):
        assert db_insert_level(1, "Easy", {"config": 1}) is None

def test_db_insert_level_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.levels.get_db_connection", return_value=conn):
        assert db_insert_level(1, "Easy", {"config": 1}) is None

def test_db_read_level_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.levels.get_db_connection", return_value=conn):
        db_read_level(1)

def test_db_read_level_fail_conn():
    with patch("database.levels.get_db_connection", return_value=None):
        assert db_read_level(1) is None

def test_db_read_level_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.levels.get_db_connection", return_value=conn):
        assert db_read_level(1) is None

def test_db_update_level_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.levels.get_db_connection", return_value=conn):
        assert db_update_level(1, "difficulty", "Hard") is True
        assert db_update_level(1, "configuration", {"new": 1}) is True

def test_db_update_level_fail_conn():
    with patch("database.levels.get_db_connection", return_value=None):
        assert db_update_level(1, "difficulty", "Hard") is None

def test_db_update_level_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.levels.get_db_connection", return_value=conn):
        assert db_update_level(1, "difficulty", "Hard") is None

def test_db_delete_level_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.levels.get_db_connection", return_value=conn):
        assert db_delete_level(1) is True

def test_db_delete_level_fail_conn():
    with patch("database.levels.get_db_connection", return_value=None):
        assert db_delete_level(1) is None

def test_db_delete_level_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.levels.get_db_connection", return_value=conn):
        assert db_delete_level(1) is None

# --- User Achievements ---
def test_db_insert_user_achievement_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.user_achievements.get_db_connection", return_value=conn):
        assert db_insert_user_achievement(1, 1, True, "2024-01-01", 5) is True

def test_db_insert_user_achievement_fail_conn():
    with patch("database.user_achievements.get_db_connection", return_value=None):
        assert db_insert_user_achievement(1, 1, True, "2024-01-01", 5) is None

def test_db_insert_user_achievement_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.user_achievements.get_db_connection", return_value=conn):
        assert db_insert_user_achievement(1, 1, True, "2024-01-01", 5) is None

def test_db_read_user_achievement_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.user_achievements.get_db_connection", return_value=conn):
        db_read_user_achievement(1, 1)

def test_db_read_user_achievement_fail_conn():
    with patch("database.user_achievements.get_db_connection", return_value=None):
        assert db_read_user_achievement(1, 1) is None

def test_db_read_user_achievement_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.user_achievements.get_db_connection", return_value=conn):
        assert db_read_user_achievement(1, 1) is None

def test_db_update_user_achievement_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.user_achievements.get_db_connection", return_value=conn):
        assert db_update_user_achievement(1, 1, "current", 10) is True

def test_db_update_user_achievement_fail_conn():
    with patch("database.user_achievements.get_db_connection", return_value=None):
        assert db_update_user_achievement(1, 1, "current", 10) is None

def test_db_update_user_achievement_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.user_achievements.get_db_connection", return_value=conn):
        assert db_update_user_achievement(1, 1, "current", 10) is None

def test_db_delete_user_achievement_success(mock_conn):
    conn, cur = mock_conn
    with patch("database.user_achievements.get_db_connection", return_value=conn):
        assert db_delete_user_achievement(1, 1) is True

def test_db_delete_user_achievement_fail_conn():
    with patch("database.user_achievements.get_db_connection", return_value=None):
        assert db_delete_user_achievement(1, 1) is None

def test_db_delete_user_achievement_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.user_achievements.get_db_connection", return_value=conn):
        assert db_delete_user_achievement(1, 1) is None

# --- Metrics ---
def test_db_get_player_full_metrics_id(mock_conn):
    conn, cur = mock_conn
    cur.fetchone.return_value = {"id": 1, "nombre": "test", "grupo": "A"}
    cur.fetchall.return_value = []
    with patch("database.metrics.get_db_connection", return_value=conn):
        res = db_get_player_full_metrics(1)
        assert res["resumen"]["id"] == 1

def test_db_get_player_full_metrics_username(mock_conn):
    conn, cur = mock_conn
    cur.fetchone.return_value = {"id": 1, "nombre": "test", "grupo": "A"}
    cur.fetchall.return_value = []
    with patch("database.metrics.get_db_connection", return_value=conn):
        res = db_get_player_full_metrics("testuser")
        assert res["resumen"]["nombre"] == "test"

def test_db_get_player_full_metrics_not_found(mock_conn):
    conn, cur = mock_conn
    cur.fetchone.return_value = None
    with patch("database.metrics.get_db_connection", return_value=conn):
        res = db_get_player_full_metrics(99)
        assert res["resumen"] is None

def test_db_get_player_full_metrics_fail_conn():
    with patch("database.metrics.get_db_connection", return_value=None):
        assert db_get_player_full_metrics(1) is None

def test_db_get_player_full_metrics_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.metrics.get_db_connection", return_value=conn):
        assert db_get_player_full_metrics(1) is None

def test_db_get_all_recent_sessions_success(mock_conn):
    conn, cur = mock_conn
    cur.fetchall.return_value = [{"id": 1}]
    with patch("database.metrics.get_db_connection", return_value=conn):
        assert db_get_all_recent_sessions() == [{"id": 1}]

def test_db_get_all_recent_sessions_fail_conn():
    with patch("database.metrics.get_db_connection", return_value=None):
        assert db_get_all_recent_sessions() is None

def test_db_get_all_recent_sessions_exception(mock_conn):
    conn, cur = mock_conn
    cur.execute.side_effect = Exception("Error")
    with patch("database.metrics.get_db_connection", return_value=conn):
        assert db_get_all_recent_sessions() is None

# --- Main 100% Coverage ---
def test_main_entry_point():
    import runpy
    from unittest.mock import patch
    with patch("main.Flask.run") as mock_run:
        try:
            runpy.run_module("main", run_name="__main__")
        except Exception:
            pass
        mock_run.assert_called_once()
