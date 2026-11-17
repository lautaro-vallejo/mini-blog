# Mar del Plata Futbolera — FastAPI Mini Blog

API REST de un mini blog sobre el fútbol de Mar del Plata: Aldosivi, Alvarado, la Liga Marplatense, los torneos de verano y la historia del estadio Minella.

Proyecto de la materia **Desarrollo de Sistemas Web (3° año)**, construido sobre el repositorio base [cgldev/fastapi-miniblog](https://github.com/cgldev/fastapi-miniblog) siguiendo los módulos 5 a 12, listo para desplegar en Render.

## Funcionalidades

| Módulo | Qué incluye |
|---|---|
| 5 · Arquitectura | Capas router / repository / schemas por dominio, `core/db.py`, application factory |
| 6 · Seguridad | `OAuth2PasswordBearer`, JWT con PyJWT y rutas protegidas con `Depends` |
| 7 · Sync/Async | Endpoints de demo `/posts/sync` y `/posts/async` + `scripts/test_async.py` |
| 8 · Archivos | Subida de imágenes (PNG/JPEG, nombre UUID, límite de MB) servidas en `/media` |
| 9 · Tags | CRUD de tags, fix de tags separados por comas, paginación global (`services/pagination.py`) y tag más popular |
| 10 · Usuarios | Modelo `User`, contraseñas con **pwdlib (Argon2)**, JWT, registro/login y roles `user` < `editor` < `admin` |
| 11 · Categorías | Categorías con slug (1 a N con posts), `ON DELETE SET NULL`, filtro de posts por categoría |
| 12 · Seeds y slugs | Slug automático y único para cada post, `GET /posts/post/{slug}` y CLI de seeds con Typer |

## Tecnologías

Python · FastAPI · Pydantic v2 · SQLAlchemy 2 · SQLite · PyJWT · pwdlib · python-slugify · Typer

## Estructura

```text
render.yaml        Blueprint para Render
scripts/           test_async.py (Módulo 7)
app/
├── main.py
├── core/          config.py · db.py · security.py
├── models/        user.py · post.py · tag.py · category.py
├── services/      file_storage.py · pagination.py
├── utils/         slugify_utils.py
├── seeds/         data.py · service.py · run.py · __main__.py
└── api/v1/
    ├── auth/        router.py · schemas.py
    ├── users/       router.py · repository.py · schemas.py
    ├── posts/       router.py · repository.py · schemas.py
    ├── tags/        router.py · repository.py · schemas.py
    ├── categories/  router.py · repository.py · schemas.py
    └── uploads/     router.py
```

## Instalación (Windows, PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env   # y cambiá JWT_SECRET
```

> Si ya tenías un `blog.db` de módulos anteriores, borralo: el esquema cambió (usuarios, categorías y slug) y `create_all` no modifica tablas existentes.

## Cargar datos de ejemplo (seeds)

```powershell
python -m app.seeds all          # todo
python -m app.seeds users        # solo usuarios
python -m app.seeds categories   # solo categorías
python -m app.seeds tags         # solo tags
python -m app.seeds posts        # posts (y sus dependencias)
```

Los seeds son idempotentes: se pueden ejecutar varias veces sin duplicar datos.

Usuarios de desarrollo:

| Email | Contraseña | Rol |
|---|---|---|
| `admin@mdpfutbolera.com` | `Admin1234!` | admin |
| `editor@mdpfutbolera.com` | `Editor1234!` | editor |
| `hincha@mdpfutbolera.com` | `Hincha1234!` | user |

> Son claves solo para desarrollo. Se pueden cambiar con `SEED_ADMIN_PASSWORD`, `SEED_EDITOR_PASSWORD` y `SEED_USER_PASSWORD`.

## Ejecutar la API

```powershell
fastapi dev app/main.py
```

Documentación: `http://127.0.0.1:8000/docs`. Para autenticarte, usá **Authorize** y poné el email en el campo `username`.

## Módulo 7: probar sync vs async

Con la API corriendo, en otra terminal:

```powershell
python scripts/test_async.py async   # 4 peticiones simultáneas a /posts/async
python scripts/test_async.py sync    # lo mismo contra /posts/sync
```

Las esperas suman 26 s, pero el tiempo total ronda los 9.7 s (lo que tarda la más lenta).

## Deploy en Render

### Opción A: Blueprint (automático)

1. Subí el proyecto a tu GitHub.
2. En Render: **New → Blueprint** y elegí el repositorio. Render lee `render.yaml` y crea la base PostgreSQL y el servicio web, con `DATABASE_URL` conectada y un `JWT_SECRET` generado.

### Opción B: manual (como en la práctica guiada)

1. **New → Postgres** (plan Free). Copiá la *Internal Database URL*.
2. **New → Web Service** con tu repositorio:
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Health Check Path: `/health`
3. En **Environment** agregá:
   - `DATABASE_URL` = la Internal Database URL
   - `JWT_SECRET` = un texto largo y aleatorio (`python -c "import secrets; print(secrets.token_urlsafe(48))"`)
   - `JWT_ALG` = `HS256`

La app acepta la URL tal como la da Render (`postgres://` o `postgresql://`) y la adapta sola al driver `psycopg2` del `requirements.txt`. Las tablas se crean al arrancar.

### Cargar los seeds en Render

El plan gratuito no tiene consola, así que los seeds se corren **desde tu PC** apuntando a la base de Render con la *External Database URL*:

```powershell
$env:DATABASE_URL = "postgresql://...external-url..."
$env:SEED_ADMIN_PASSWORD  = "una-clave-tuya"
$env:SEED_EDITOR_PASSWORD = "otra-clave-tuya"
$env:SEED_USER_PASSWORD   = "otra-mas"
python -m app.seeds all
Remove-Item Env:DATABASE_URL   # para volver a tu base local
```

> ⚠️ No uses las claves de ejemplo en Render: están publicadas en este README y cualquiera podría entrar como admin.

### Limitaciones del plan gratuito de Render

- El servicio se duerme tras 15 minutos sin tráfico; la primera petición después tarda cerca de un minuto.
- El disco es efímero: las **imágenes subidas a `/media` se pierden** en cada redeploy, reinicio o cuando se duerme. Los datos de la base sí se conservan.
- La base PostgreSQL gratuita **vence a los 30 días** de creada.

## Endpoints (prefijo `/api/v1`)

| Método | Ruta | Permiso | Propósito |
|---|---|---|---|
| `POST` | `/auth/register` | público | Registrar usuario (rol `user`) |
| `POST` | `/auth/login` | público | Login por formulario (Swagger) |
| `POST` | `/auth/login/json` | público | Login con JSON `{email, password}` |
| `GET` | `/auth/me` | logueado | Mi perfil |
| `GET` | `/users` | admin | Listar usuarios (paginado, `?search=`) |
| `GET` | `/users/{id}` | admin | Ver usuario |
| `PATCH` | `/users/{id}/role` | admin | Cambiar rol |
| `PATCH` | `/users/{id}/status` | admin | Activar / desactivar |
| `DELETE` | `/users/{id}` | admin | Eliminar usuario |
| `GET` | `/posts` | público | Listar (búsqueda, paginación, orden, `?category=slug`) |
| `GET` | `/posts/by-tags` | público | Filtrar por tags |
| `GET` | `/posts/sync` · `/posts/async` | público | Demo del Módulo 7 (`?t=segundos`) |
| `GET` | `/posts/post/{slug}` | público | Ver post por slug |
| `GET` | `/posts/{id}` | público | Ver post por id |
| `POST` | `/posts` | editor | Crear post (multipart: título, contenido, `category_id`, tags, imagen) |
| `PUT` | `/posts/{id}` | editor (propio) / admin | Actualizar post |
| `DELETE` | `/posts/{id}` | editor (propio) / admin | Eliminar post |
| `GET` | `/tags` | público | Listar tags (paginado) |
| `GET` | `/tags/popular` | público | Tag más usado |
| `GET` | `/tags/{id}` | público | Ver tag |
| `POST` / `PUT` | `/tags` · `/tags/{id}` | editor | Crear / renombrar tag |
| `DELETE` | `/tags/{id}` | admin | Eliminar tag |
| `GET` | `/categories` | público | Listar categorías |
| `GET` | `/categories/{id}` · `/categories/slug/{slug}` | público | Ver categoría |
| `POST` / `PATCH` | `/categories` · `/categories/{id}` | editor | Crear / editar categoría |
| `DELETE` | `/categories/{id}` | admin | Eliminar categoría (los posts quedan sin categoría) |
| `POST` | `/upload/save` | público | Subir una imagen suelta |

Las imágenes quedan accesibles en `/media/<archivo>`. Además: `GET /` (info) y `GET /health` (chequeo de Render).

## Autor

Proyecto base: César Gimenez Lascano — [@cgldev](https://github.com/cgldev)
