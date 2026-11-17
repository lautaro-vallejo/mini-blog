from math import ceil
from typing import Any, Dict, Optional, Sequence

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session


def paginate_query(
    db: Session,
    model,
    base_query: Optional[Select] = None,
    page: int = 1,
    per_page: int = 10,
    order_by: Optional[str] = None,
    direction: str = "asc",
    allowed_order: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Pagina cualquier modelo (Posts, Tags, Usuarios...) con una sola llamada.

    - base_query: consulta con filtros ya aplicados (si es None, se usa select(model)).
    - allowed_order: diccionario {"nombre_publico": columna} para ordenar de forma segura.
    """
    query = base_query if base_query is not None else select(model)

    # Contamos sobre la consulta filtrada (no sobre toda la tabla)
    total = db.scalar(select(func.count()).select_from(
        query.order_by(None).subquery())) or 0

    pages = ceil(total / per_page) if total > 0 else 0
    current_page = 1 if pages == 0 else min(max(page, 1), pages)

    # Ordenamiento: solo columnas permitidas
    allowed_order = allowed_order or {"id": model.id}
    order_col = allowed_order.get(order_by) if order_by else None
    if order_col is None:
        order_col = model.id
    query = query.order_by(
        order_col.desc() if direction == "desc" else order_col.asc())

    items: Sequence = []
    if total > 0:
        items = db.execute(
            query.offset((current_page - 1) * per_page).limit(per_page)
        ).scalars().unique().all()

    return {
        "total": total,
        "items": items,
        "pages": pages,
        "page": current_page,
        "per_page": per_page,
        "has_prev": current_page > 1,
        "has_next": current_page < pages,
    }
