from flask import Flask, request, send_from_directory, Blueprint
from database.users import db_insert_user, db_delete_user, db_read_user_by_id, db_read_user, db_update_user
from database.levels import db_insert_level, db_read_level, db_update_level, db_delete_level
from database.achievements import db_insert_achievement, db_read_achievement, db_update_achievement, db_delete_achievement
from database.game_sessions import db_insert_game_session, db_read_game_session, db_update_game_session, db_delete_game_session
from database.user_achievements import db_insert_user_achievement, db_read_user_achievement, db_update_user_achievement, db_delete_user_achievement
from database.metrics import db_get_player_full_metrics, db_get_all_recent_sessions

from dotenv import load_dotenv
from werkzeug.security import check_password_hash

api = Blueprint('api', __name__, url_prefix='/api')

# --- USER CRUD ---
@api.post("/users")
def registrar_usuario():
    try:
        data = request.get_json()
        user_insert = db_insert_user(data.get("username"), data.get(
            "mail"), data.get("password"), data.get("rol"), data.get("group", ""))
        if user_insert is None:
            return {"status": "fail", "message": "Usuario no pudo ser registrado"}, 500
        return {"status": "exitoso", "message": "Usuario registrado con exito"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.delete("/users")
def delete_usuario():
    try:
        user_id = request.get_json().get('user_id')
        if db_delete_user(user_id) is None:
             return {"status": "fail", "message": "Usuario no pudo ser eliminado"}, 500
        return {"status": "successful", "message": f"Usuario {user_id} eliminado con exito"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.get("/users/<int:user_id>")
def get_usuario(user_id):
    try:
        user = db_read_user_by_id(user_id)
        if not user:
             return {"status": "fail", "message": "Usuario no encontrado"}, 404
        return {"status": "successful", "user": user}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.put("/users/<int:user_id>")
def update_usuario(user_id):
    try:
        data = request.get_json()
        if db_update_user(user_id, data.get("parameter"), data.get("value")) is None:
             return {"status": "fail", "message": "No se pudo actualizar"}, 500
        return {"status": "successful", "parameter": data.get("parameter"), "new_value": data.get("value")}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

# --- LOGIN ---
@api.route("/users/login", methods=["POST"])
def validar_usuario():
    try:
        data = request.get_json()
        sql_data = db_read_user(data.get("username"))
        if not sql_data:
            return {"valido": False, "message": "Usuario no encontrado"}, 404

        hashed_password = sql_data[0]["password"]
        user_id = sql_data[0]["id"]
        user_rol = sql_data[0]["rol"]
        if check_password_hash(hashed_password, data.get("password")):
            return {"valido": True, "userId": user_id, "rol": user_rol}, 200
        return {"valido": False, "message": "Contraseña invalida"}, 401
    except Exception as e:
        return {"valido": False, "error_message": str(e)}, 401

# --- METRICS ---
@api.get("/metrics/player/<string:identifier>")
def get_metrics_individual(identifier):
    data = db_get_player_full_metrics(identifier)
    if not data or not data['resumen']:
        return {"status": "fail", "message": "No se encontraron datos"}, 404

    def fmt_time(segundos):
        if not segundos: return "00:00"
        m, s = divmod(int(segundos), 60)
        return f"{m:02d}:{s:02d}"

    data['resumen']['tiempo_total'] = fmt_time(
        data['resumen']['tiempo_total_segundos'])
    for s in data['sesiones']:
        s['tiempo'] = fmt_time(s['tiempo'])

    return data, 200

@api.get("/metrics/recent")
def get_metrics_recent():
    sessions = db_get_all_recent_sessions()
    if sessions is None:
        return {"status": "error"}, 500
    return {"sessions": sessions}, 200

# ---------BORRAR AQUI---------
@api.get("/clases")
def get_clases():
    maestro_id = request.args.get("maestro_id")
    maestroId = request.args.get("maestroId")
    m_id = maestro_id or maestroId
    conn = None

    try:
        from database.connection import get_db_connection
        conn = get_db_connection()

        if conn is None:
            return {"status": "error", "message": "No connection to database"}, 500

        cur = conn.cursor()

        cur.execute(
            'SELECT DISTINCT "group" FROM users WHERE "group" IS NOT NULL')
        grupos = cur.fetchall()

        clases_list = [{"id": str(g['group']), "nombre": f"Grupo {g['group']}"} for g in grupos]

        return {"status": "successful", "clases": clases_list}

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

    finally:
        if conn:
            conn.close()

@api.post("/clases")
def crear_clase():
    try:
        data = request.get_json()

        username = data.get("username")
        maestro_id = data.get("maestro_id")

        if not username or not maestro_id:
            return {"status": "fail", "messsage": "Faltan datos obligatorios"}, 400

        from database.clases import db_insert_clase
        if db_insert_clase(username, maestro_id) is None:
            return {"status": "fail", "message": "No se pudo crear la clase"}, 500

        return {"status": "exitoso", "message": "Clase creada correctamente"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

# ------HASTA ACA--------------

@api.get("/metrics/clase/<string:clase_id>")
def get_metrics_clase(clase_id):
    try:
        from database.connection import get_db_connection
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            SELECT s.time_played, s.score, u.username, u.id
            FROM game_sessions s
            JOIN users u ON s.user_id = u.id
            WHERE u."group" = %s
        """
        cur.execute(query, (clase_id,))
        rows = cur.fetchall()

        return {
            "status": "successful",
            "clase": clase_id,
            "data": {
                "tiempos": [r['time_played'] for r in rows],
                "puntajes": [r['score'] for r in rows],
                "alumnos": [r['username'] for r in rows],
                "ids": [r['id'] for r in rows]
        }
        }, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400
    finally:
        if 'conn' in locals() and conn: conn.close()


# --- ACHIEVEMENTS CRUD ---
@api.post("/achievements")
def create_achievement():
    try:
        data = request.get_json()
        if db_insert_achievement(data.get("name"), data.get("description"), data.get("goal")) is None:
            return {"status": "fail", "message": "Logro no pudo ser registrado"}, 500
        return {"status": "exitoso"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.get("/achievements/<int:achievement_id>")
def get_achievement(achievement_id):
    try:
        ach = db_read_achievement(achievement_id)
        if not ach: return {"status": "fail", "message": "Logro no encontrado"}, 404
        return {"status": "successful", "achievement": ach}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.put("/achievements/<int:achievement_id>")
def update_achievement(achievement_id):
    try:
        data = request.get_json()
        if db_update_achievement(achievement_id, data.get("parameter"), data.get("value")) is None:
            return {"status": "fail", "message": "No se pudo actualizar"}, 500
        return {"status": "successful"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.delete("/achievements")
def delete_achievement():
    try:
        achievement_id = request.get_json().get("achievement_id")
        if db_delete_achievement(achievement_id) is None:
            return {"status": "fail", "message": "No se pudo eliminar"}, 500
        return {"status": "successful"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

# --- LEVELS CRUD ---
@api.post("/levels")
def create_level():
    try:
        data = request.get_json()
        if db_insert_level(data.get("level_num"), data.get("difficulty"), data.get("configuration")) is None:
            return {"status": "fail", "message": "Nivel no pudo ser registrado"}, 500
        return {"status": "exitoso"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.get("/levels/<int:level_id>")
def get_level(level_id):
    try:
        lvl = db_read_level(level_id)
        if not lvl: return {"status": "fail", "message": "Nivel no encontrado"}, 404
        return {"status": "successful", "level": lvl}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.put("/levels/<int:level_id>")
def update_level(level_id):
    try:
        data = request.get_json()
        if db_update_level(level_id, data.get("parameter"), data.get("value")) is None:
            return {"status": "fail", "message": "No se pudo actualizar"}, 500
        return {"status": "successful"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.delete("/levels")
def delete_level():
    try:
        level_id = request.get_json().get("level_id")
        if db_delete_level(level_id) is None:
            return {"status": "fail", "message": "No se pudo eliminar"}, 500
        return {"status": "successful"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

# --- GAME SESSIONS CRUD ---
@api.post("/sessions")
def create_session():
    try:
        data = request.get_json()
        if db_insert_game_session(data.get("user_id"), data.get("level_id"), data.get("completed"), data.get("time_played"), data.get("score"), data.get("date")) is None:
            return {"status": "fail", "message": "Sesion no pudo ser registrada"}, 500
        return {"status": "exitoso"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.get("/sessions/<int:session_id>")
def get_session(session_id):
    try:
        sess = db_read_game_session(session_id)
        if not sess: return {"status": "fail", "message": "Sesion no encontrada"}, 404
        return {"status": "successful", "session": sess}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.put("/sessions/<int:session_id>")
def update_session(session_id):
    try:
        data = request.get_json()
        if db_update_game_session(session_id, data.get("parameter"), data.get("value")) is None:
            return {"status": "fail", "message": "No se pudo actualizar"}, 500
        return {"status": "successful"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.delete("/sessions")
def delete_session():
    try:
        session_id = request.get_json().get("session_id")
        if db_delete_game_session(session_id) is None:
            return {"status": "fail", "message": "No se pudo eliminar"}, 500
        return {"status": "successful"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

# --- USER ACHIEVEMENTS CRUD ---
@api.post("/user_achievements")
def create_user_achievement():
    try:
        data = request.get_json()
        if db_insert_user_achievement(data.get("user_id"), data.get("achievement_id"), data.get("unlocked"), data.get("date_unlocked"), data.get("current")) is None:
            return {"status": "fail", "message": "User achievement no pudo ser registrado"}, 500
        return {"status": "exitoso"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.get("/user_achievements/<int:user_id>/<int:achievement_id>")
def get_user_achievement(user_id, achievement_id):
    try:
        u_ach = db_read_user_achievement(user_id, achievement_id)
        if not u_ach: return {"status": "fail", "message": "No encontrado"}, 404
        return {"status": "successful", "user_achievement": u_ach}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.put("/user_achievements/<int:user_id>/<int:achievement_id>")
def update_user_achievement(user_id, achievement_id):
    try:
        data = request.get_json()
        if db_update_user_achievement(user_id, achievement_id, data.get("parameter"), data.get("value")) is None:
            return {"status": "fail", "message": "No se pudo actualizar"}, 500
        return {"status": "successful"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.delete("/user_achievements")
def delete_user_achievement():
    try:
        data = request.get_json()
        if db_delete_user_achievement(data.get("user_id"), data.get("achievement_id")) is None:
            return {"status": "fail", "message": "No se pudo eliminar"}, 500
        return {"status": "successful"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 400

@api.route("/api/<path:filename>", methods=["GET"])
def api_files(filename):
    return send_from_directory("api", filename)

@api.route("/")
def index():
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <title>Memoretos - Panel de Control Unificado</title>
    <style>
        body {
            background-color: #111827;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            padding: 20px;
            margin: 0;
        }
        .container { max-width: 1200px; margin: auto; }
        .selector-section {
            background-color: #1f2937;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #374151;
            margin-bottom: 30px;
            text-align: center;
        }
        select, button {
            padding: 10px 15px;
            border-radius: 8px;
            border: none;
            font-size: 1rem;
        }
        select { background-color: #374151; color: white; margin-right: 10px; }
        button {
            background-color: #10b981;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover { background-color: #059669; }
        .grafica {
            width: 100%;
            height: 45vh;
            margin-bottom: 30px;
            border: 1px solid #374151;
            border-radius: 12px;
            padding: 15px;
            background-color: #1f2937;
        }
        h1 { text-align: center; color: #10b981; }
        h2 { font-size: 1.2rem; color: #9ca3af; }
        #statsList ul {
            list-style: none;
            padding: 0;
            display: flex;
            justify-content: center;
            gap: 20px;
            color: #fbbf24;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Dashboard Memoretos</h1>

        <div class="selector-section">
            <h2>Consulta Rápida por Nivel</h2>
            <label for="nivelSelect">Nivel: </label>
            <select id="nivelSelect">
                <option value="1">Nivel 1 (Easy)</option>
                <option value="2">Nivel 2 (Medium)</option>
                <option value="3">Nivel 3 (Hard)</option>
            </select>
            <button id="loadStatsBtn">Cargar Datos</button>
            <div id="statsList"></div>
        </div>

        <h2>Análisis de Tiempos (Grupo A vs B)</h2>
        <div id="graficaTiempos" class="grafica"></div>

        <h2>Progreso de Niveles</h2>
        <div id="graficaProgreso" class="grafica"></div>
    </div>

    <script>
        document.getElementById("loadStatsBtn").addEventListener("click", function() {
            const nivelId = document.getElementById("nivelSelect").value;
            fetch(`/estadisticas/${nivelId}`)
            .then(response => response.json())
            .then(data => {
                const statsList = document.getElementById("statsList");
                if (data.estadisticas) {
                    const stats = data.estadisticas;
                    statsList.innerHTML = `<ul>
                        <li><b>Dificultad:</b> ${stats.dificultad}</li>
                        <li><b>Máximo:</b> ${stats.score_maximo} pts</li>
                        <li><b>Promedio:</b> ${stats.tiempo_promedio}s</li>
                        <li><b>Intentos:</b> ${stats.total_intentos}</li>
                    </ul>`;
                }
            });
        });

        var x_niveles = ['Nivel 1', 'Nivel 1', 'Nivel 1', 'Nivel 2', 'Nivel 2', 'Nivel 2', 'Nivel 3', 'Nivel 3', 'Nivel 3'];
        var traceTiemposA = {
            y: [20, 25, 22, 70, 75, 72, 180, 195, 188], x: x_niveles,
            name: 'Grupo A', type: 'box', marker: {color: '#10b981'}
        };
        var traceTiemposB = {
            y: [35, 42, 38, 95, 105, 100, 240, 260, 255], x: x_niveles,
            name: 'Grupo B', type: 'box', marker: {color: '#3b82f6'}
        };
        Plotly.newPlot('graficaTiempos', [traceTiemposA, traceTiemposB], {
            paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
            font: {color: '#d1d5db'}, boxmode: 'group', margin: {t:10}
        });

        var x_grupos = ['Grupo A', 'Grupo A', 'Grupo A', 'Grupo A', 'Grupo B', 'Grupo B', 'Grupo B', 'Grupo B'];
        var traceProgreso = {
            y: [25, 28, 30, 22, 10, 12, 15, 8], x: x_grupos,
            name: 'Niveles', type: 'box', marker: {color: '#f59e0b'}, boxpoints: 'all'
        };
        Plotly.newPlot('graficaProgreso', [traceProgreso], {
            paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
            font: {color: '#d1d5db'}, margin: {t:10}
        });
    </script>
</body>
</html>
"""

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv(override=True)
    app.register_blueprint(api)
    return app

app = create_app()
application = app

if __name__ == "__main__":
    app.run(debug=True, port=18462)