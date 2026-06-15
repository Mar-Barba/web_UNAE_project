from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import get_db_connection
import psycopg2


def db_insert_user(username: str, mail:str, password:str, rol:str, group:str = ""):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        hash_password = generate_password_hash(password)
        cur = conn.cursor()
        query = 'INSERT INTO users (username, mail, password, rol, "group") VALUES (%s, %s, %s, %s, %s)'
        cur.execute(query, (username, mail, hash_password, rol, group))
        conn.commit()
        return True
    except psycopg2.Error as e:
        if conn: conn.rollback()
        error_msg = f'DB Error: {e.pgerror}, code: {e.pgcode}'
        print(error_msg)
        return None
    except Exception as e:
        if conn: conn.rollback()
        error_msg = f'Unexpected Error: {e}'
        print(error_msg)
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_delete_user(user_id: int):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_read_user(username: str):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cur.fetchall()
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_read_user_by_id(user_id: int):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cur.fetchall()
    except Exception as e:
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_update_user(user_id: int, parameter: str, value):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        query = f"UPDATE users SET {parameter} = %s WHERE id = %s"
        cur.execute(query, (value, user_id))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()