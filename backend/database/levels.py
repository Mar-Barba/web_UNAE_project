from flask import jsonify
from database.connection import get_db_connection
import psycopg2
import json

def db_insert_level(num_nivel: int, dificultad: str, configuracion: dict):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        query = 'INSERT INTO levels (level_num, difficulty, configuration) VALUES (%s, %s, %s)'
        cur.execute(query, (num_nivel, dificultad, json.dumps(configuracion)))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_read_level(level_id: int):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM levels WHERE id = %s", (level_id,))
        return cur.fetchall()
    except Exception as e:
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_update_level(level_id: int, parameter: str, value):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        if parameter == 'configuration':
            value = json.dumps(value)
        query = f"UPDATE levels SET {parameter} = %s WHERE id = %s"
        cur.execute(query, (value, level_id))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_delete_level(level_id: int):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM levels WHERE id = %s", (level_id,))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()
