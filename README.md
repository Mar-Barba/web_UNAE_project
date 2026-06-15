# Memoretos - Equipo 6

---

Equipo:

- Armando Vasquez Ambrocio A01669283
- Atl Andrés Torres Flores A01668629
- Marbella Barba De los Santos A01660946
- Miguel Ángel Garduño Manrique A01668481
- Rafael Antonio Carrión Ortega A01660812
  v2.0
url final: https://memoretos.atoligue.uber.space/api

---

## 🚀 Cómo correr el proyecto con Docker

Este proyecto está completamente contenedorizado. Sigue estos pasos para levantarlo localmente:

### 1. Requisitos previos

Asegúrate de tener un archivo `.env` en la raíz del proyecto con las credenciales necesarias (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`).

```bash
touch .env
nano .env
```

DATABASE_URL=postgresql://admin:tecmemoreto@db:5432/memoretos

POSTGRES_USER=postgres
POSTGRES_PASSWORD=tecmemoreto
POSTGRES_DB=memoretos

### 2. Levantar el proyecto

Para construir e iniciar todos los servicios (Base de Datos, Backend y Frontend) en segundo plano:

```bash
docker compose up -d
```

- **Frontend:** Disponible en [http://localhost:8080/login](http://localhost:8080/login)
- **Backend:** Disponible en [http://localhost:5000](http://localhost:5000)

## 🗄️ Acceso a la Base de Datos

Para interactuar directamente con la base de datos PostgreSQL que corre dentro del contenedor, usa el siguiente comando:

```bash
docker exec -it postgres_local psql -U postgres -d memoretos
```

### Comandos útiles dentro de psql:

- `\dt` : Listar todas las tablas.
- `\d nombre_tabla` : Ver la estructura de una tabla específica.
- `SELECT * FROM users;` : Consultar datos de la tabla de usuarios.
- `\q` : Salir de la terminal de PostgreSQL.

---

### 🛑 Detener el proyecto

Para apagar los contenedores pero mantener los datos de la base de datos:

```bash
docker compose stop
```

Para eliminar los contenedores (los datos persistirán en el volumen `db_data`):

```bash
docker compose down
```
