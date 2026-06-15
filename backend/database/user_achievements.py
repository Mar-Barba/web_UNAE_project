from flask import jsonify
from database.connection import get_db_connection
import psycopg2
import json

def db_insert_user_achievement(user_id: int, achievement_id: int, unlocked: bool, date_unlocked: str, current: int):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        query = 'INSERT INTO user_achievements (user_id, achievement_id, unlocked, date_unlocked, current) VALUES (%s, %s, %s, %s, %s)'
        cur.execute(query, (user_id, achievement_id, unlocked, date_unlocked, current))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_read_user_achievement(user_id: int, achievement_id: int):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_achievements WHERE user_id = %s AND achievement_id = %s", (user_id, achievement_id))
        return cur.fetchall()
    except Exception as e:
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_update_user_achievement(user_id: int, achievement_id: int, parameter: str, value):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        query = f"UPDATE user_achievements SET {parameter} = %s WHERE user_id = %s AND achievement_id = %s"
        cur.execute(query, (value, user_id, achievement_id))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()

def db_delete_user_achievement(user_id: int, achievement_id: int):
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM user_achievements WHERE user_id = %s AND achievement_id = %s", (user_id, achievement_id))
        conn.commit()
        return True
    except Exception as e:
        if conn: conn.rollback()
        print(f'Unexpected Error: {e}')
        return None
    finally:
        if 'cur' in locals(): cur.close()
        if conn: conn.close()
