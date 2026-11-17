# Mar del Plata Futbolera — FastAPI Mini Blog

API REST de un mini blog sobre el fútbol de Mar del Plata: Aldosivi, Alvarado, la Liga Marplatense, los torneos de verano y la historia del estadio Minella.

Proyecto de la materia **Desarrollo de Sistemas Web (3° año)**, construido sobre el repositorio base [cgldev/fastapi-miniblog](https://github.com/cgldev/fastapi-miniblog) siguiendo los módulos 8 a 12.

## Funcionalidades

| Módulo | Qué incluye |
|---|---|
| 8 · Archivos | Subida de imágenes (PNG/JPEG, nombre UUID, límite de MB) servidas en `/media` |
| 9 · Tags | CRUD de tags, fix de tags separados por comas, paginación global (`services/pagination.py`) y tag más popular |
| 10 · Usuarios | Modelo `User`, contraseñas con **pwdlib (Argon2)**, JWT, registro/login y roles `user` < `editor` < `admin` |
| 11 · Categorías | Categorías con slug (1 a N con posts), `ON DELETE SET NULL`, filtro de posts por categoría |
| 12 · Seeds y slugs | Slug automático y único para cada post, `GET /posts/post/{slug}` y CLI de seeds con Typer |

## Tecnologías

Python · FastAPI · Pydantic v2 · SQLAlchemy 2 · SQLite · PyJWT · pwdlib · python-slugify · Typer

## Estructura

```text
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

Las imágenes quedan accesibles en `/media/<archivo>`.

## Autor

Proyecto base: César Gimenez Lascano — [@cgldev](https://github.com/cgldev)
