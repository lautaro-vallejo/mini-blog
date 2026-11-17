"""Datos iniciales de "Mar del Plata Futbolera".

Las contraseñas se pueden pisar con variables de entorno (SEED_ADMIN_PASSWORD, etc.).
Son datos de DESARROLLO: no usar estas claves en producción.
"""
import os

USERS = [
    {
        "email": "admin@mdpfutbolera.com",
        "username": "admin",
        "password": os.getenv("SEED_ADMIN_PASSWORD", "Admin1234!"),
        "role": "admin",
    },
    {
        "email": "editor@mdpfutbolera.com",
        "username": "cronista_costero",
        "password": os.getenv("SEED_EDITOR_PASSWORD", "Editor1234!"),
        "role": "editor",
    },
    {
        "email": "hincha@mdpfutbolera.com",
        "username": "hincha_marplatense",
        "password": os.getenv("SEED_USER_PASSWORD", "Hincha1234!"),
        "role": "user",
    },
]

CATEGORIES = [
    {"name": "Aldosivi", "slug": "aldosivi"},
    {"name": "Alvarado", "slug": "alvarado"},
    {"name": "Liga Marplatense", "slug": "liga-marplatense"},
    {"name": "Torneos de Verano", "slug": "torneos-de-verano"},
    {"name": "Historia y Estadios", "slug": "historia-y-estadios"},
]

TAGS = [
    "tiburon", "torito", "minella", "clasico-marplatense", "ascenso",
    "inferiores", "hinchada", "mundial-78", "previa", "potrero",
]

# Cada post referencia su categoría por slug y su autor por email
POSTS = [
    {
        "title": "El Minella, la casa mundialista de Mar del Plata",
        "content": (
            "El estadio José María Minella nació para el Mundial 1978, cuando "
            "Mar del Plata fue una de las sedes del torneo. Desde entonces es "
            "el escenario de los partidos más importantes de la ciudad: "
            "fútbol de Primera, torneos de verano y clásicos locales. "
            "En este blog vamos a recorrer su historia y las tardes que "
            "quedaron en la memoria de los marplatenses."
        ),
        "category": "historia-y-estadios",
        "tags": ["minella", "mundial-78"],
        "author": "editor@mdpfutbolera.com",
    },
    {
        "title": "Cómo se vive una tarde de Aldosivi",
        "content": (
            "La previa arranca temprano: mate, choripán y camisetas verdes y "
            "amarillas camino al estadio. El Tiburón tiene una hinchada fiel "
            "que acompaña en las buenas y en las malas. En esta nota contamos "
            "qué tenés que saber si vas por primera vez a ver a Aldosivi."
        ),
        "category": "aldosivi",
        "tags": ["tiburon", "hinchada", "minella"],
        "author": "editor@mdpfutbolera.com",
    },
    {
        "title": "Alvarado, el Torito que no afloja",
        "content": (
            "Alvarado es uno de los clubes con más historia del fútbol "
            "marplatense. Su gente vive cada partido con una pasión que "
            "contagia, y el club sigue apostando a sus divisiones inferiores "
            "para formar jugadores propios."
        ),
        "category": "alvarado",
        "tags": ["torito", "inferiores", "ascenso"],
        "author": "editor@mdpfutbolera.com",
    },
    {
        "title": "Previa del clásico marplatense",
        "content": (
            "Aldosivi y Alvarado protagonizan el clásico de la ciudad. "
            "Más allá de la tabla, es el partido que todos quieren ganar. "
            "Te dejamos las claves para seguirlo y qué esperar de cada equipo."
        ),
        "category": "liga-marplatense",
        "tags": ["clasico-marplatense", "tiburon", "torito", "previa"],
        "author": "editor@mdpfutbolera.com",
    },
    {
        "title": "Liga Marplatense: el semillero de la ciudad",
        "content": (
            "Los domingos de Liga Marplatense son puro fútbol de barrio: "
            "canchas llenas de familias, clubes que se sostienen con el "
            "esfuerzo de sus socios y pibes que sueñan con llegar a Primera. "
            "Acá arranca todo."
        ),
        "category": "liga-marplatense",
        "tags": ["potrero", "inferiores"],
        "author": "admin@mdpfutbolera.com",
    },
    {
        "title": "Torneos de verano: cuando los grandes llegan a la costa",
        "content": (
            "Cada temporada, los amistosos de verano llevan a Mar del Plata a "
            "los equipos más convocantes del país. Para muchos marplatenses "
            "es la única oportunidad de ver en vivo a sus ídolos. Repasamos "
            "por qué estos partidos son una tradición de la ciudad."
        ),
        "category": "torneos-de-verano",
        "tags": ["minella", "hinchada"],
        "author": "admin@mdpfutbolera.com",
    },
]
