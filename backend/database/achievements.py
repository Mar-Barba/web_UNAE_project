from flask import jsonify
from database.connection import get_db_connection
import psycopg2

def db_insert_achievement(name: str, description: str, goal: int):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cur = conn.cursor()
        query = 'INSERT INTO achievements (name, description, goal) VALUES (%s, %s, %s)'
        cur.execute(query, (name, description, goal))
        conn.commit()
        return True
    except psycopg2.Error as e:
        if conn: conn.rollback()
        print(f'DB Error: {e.pgerror}, code: {e.pgcode}')
        return None
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_read_achievement(achievement_id: int):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM achievements WHERE id = %s", (achievement_id,))
        return cur.fetchall()
    except Exception as e:
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_update_achievement(achievement_id: int, parameter: str, value):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        query = f"UPDATE achievements SET {parameter} = %s WHERE id = %s"
        cur.execute(query, (value, achievement_id))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_delete_achievement(achievement_id: int):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM achievements WHERE id = %s", (achievement_id,))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()
