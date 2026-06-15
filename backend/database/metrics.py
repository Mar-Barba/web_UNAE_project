from database.connection import get_db_connection
from psycopg2.extras import RealDictCursor

def db_get_player_full_metrics(identifier):
    conn = get_db_connection()
    if conn is None: return None
    try:
        # Usamos RealDictCursor para que los resultados sean {'columna': valor}
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        if str(identifier).isdigit():
            where_clause = "u.id = %s"
            param = (int(identifier),)
        else:
            where_clause = "u.username ILIKE %s" # ILIKE ignores case
            param = (str(identifier),)
            
        # 1. Obtener Resumen del Jugador
        query_resumen = f"""
            SELECT 
                u.id, u.username as nombre, u."group" as grupo,
                COUNT(s.id) as total_sesiones,
                SUM(s.time_played) as tiempo_total_segundos,
                COUNT(DISTINCT s.level_id) as retos_completados
            FROM users u
            LEFT JOIN game_sessions s ON u.id = s.user_id
            WHERE {where_clause}
            GROUP BY u.id, u.username, u."group"
        """
        cur.execute(query_resumen, param)
        resumen = cur.fetchone()
        
        if not resumen:
            return {"resumen": None, "sesiones": []}
            
        actual_user_id = resumen['id']

        query_sesiones = """
            SELECT 
                s.id as id_sesion, 
                l.level_num as memo_id, 
                s.date as fecha, 
                s.time_played as tiempo
            FROM game_sessions s
            JOIN levels l ON s.level_id = l.id
            WHERE s.user_id = %s
            ORDER BY s.date DESC
        """
        cur.execute(query_sesiones, (actual_user_id,))
        sesiones = cur.fetchall()

        return {"resumen": resumen, "sesiones": sesiones}
    except Exception as e:
        print(f"Error en metrics: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def db_get_all_recent_sessions():
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT 
                s.user_id as id_usuario, u.username as nombre, 
                l.level_num as memo_id, s.time_played as tiempo, s.date as fecha
            FROM game_sessions s
            JOIN users u ON s.user_id = u.id
            JOIN levels l ON s.level_id = l.id
            ORDER BY s.date DESC LIMIT 50
        """
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        print(f"Error en metrics: {e}")
        return None
    finally:
        cur.close()
        conn.close()