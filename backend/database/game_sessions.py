from flask import jsonify
from database.connection import get_db_connection
import psycopg2

def db_insert_game_session(user_id: int, level_id: int, completed: bool, time_played: int, score: int, date: str):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        query = 'INSERT INTO game_sessions (user_id, level_id, completed, time_played, score, date) VALUES (%s, %s, %s, %s, %s, %s)'
        cur.execute(query, (user_id, level_id, completed, time_played, score, date))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_read_game_session(session_id: int):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM game_sessions WHERE id = %s", (session_id,))
        return cur.fetchall()
    except Exception as e:
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_update_game_session(session_id: int, parameter: str, value):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        query = f"UPDATE game_sessions SET {parameter} = %s WHERE id = %s"
        cur.execute(query, (value, session_id))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_delete_game_session(session_id: int):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM game_sessions WHERE id = %s", (session_id,))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()
