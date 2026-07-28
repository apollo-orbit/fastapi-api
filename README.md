# API Chida

API simple con FastAPI para pruebas y demos.

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Mensaje de bienvenida |
| GET | `/health` | Status check |
| GET | `/items/{item_id}?q=...` | Item de prueba |
| **GET** | **`/users`** | **Lista todos los usuarios** |
| **GET** | **`/users/{user_id}`** | **Detalle de un usuario** |
| **POST** | **`/users`** | **Crear usuario** |
| **PUT** | **`/users/{user_id}`** | **Actualizar usuario** |
| **DELETE** | **`/users/{user_id}`** | **Eliminar usuario** |

## Usuarios dummy precargados

| id | Nombre | Email | Rol |
|----|--------|-------|-----|
| 1 | Alejandro Ramírez | alex@99labs.co | admin |
| 2 | María García | maria@example.com | user |
| 3 | Carlos López | carlos@example.com | user |
| 4 | Ana Torres | ana@example.com | editor |
| 5 | Luis Hernández | luis@example.com | user |

## Body para POST /users

```json
{
  "name": "Pedro Sánchez",
  "email": "pedro@example.com",
  "role": "user"
}
```

**Campos:** `name` (string), `email` (string, único), `role` (string: `admin` | `user` | `editor`)

## Body para PUT /users/{id}

```json
{
  "name": "Pedro Actualizado",
  "email": "nuevo@example.com",
  "role": "editor"
}
```

Todos los campos son opcionales. Solo se actualizan los que se envíen.

## Headers

```
Content-Type: application/json
```

No requiere autenticación. CORS habilitado para cualquier origen.

## Ejemplos con curl

**Listar usuarios:**
```bash
curl http://192.168.100.10:8000/users
```

**Crear usuario:**
```bash
curl -X POST http://192.168.100.10:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Pedro","email":"pedro@example.com","role":"user"}'
```

**Actualizar usuario:**
```bash
curl -X PUT http://192.168.100.10:8000/users/6 \
  -H "Content-Type: application/json" \
  -d '{"name":"Pedro Actualizado"}'
```

**Eliminar usuario:**
```bash
curl -X DELETE http://192.168.100.10:8000/users/6
```

## Validación de email

El email debe ser único (case-insensitive). Si intentas crear o actualizar a un email que ya existe en otro usuario, la API devuelve **409 Conflict**:

```json
{"detail": "Email 'alex@99labs.co' already exists"}
```

## Cómo correr localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Servidor en `http://localhost:8000`. Documentación interactiva en `/docs` (Swagger UI).
