from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Any

from sqlalchemy.orm import Session

from app.models.product import Category
from app.schemas.product import CategoryOut


@dataclass(frozen=True)
class _CacheEntry:
    expires_at: float
    payload: list[CategoryOut]


_CATEGORIES_CACHE: dict[str, Any] = {"entry": None}
_CACHE_KEY = "entry"
_CACHE_TTL_SECONDS = 60.0


def invalidate_categories_cache() -> None:
    """Reset the in-memory cache for public category payloads."""

    _CATEGORIES_CACHE[_CACHE_KEY] = None


def _serialize_categories(rows: list[Category]) -> list[CategoryOut]:
    return [
        CategoryOut(
            id=row.id,
            slug=row.slug,
            name=row.name,
            parent_id=row.parent_id,
        )
        for row in rows
    ]


def get_categories_payload(db: Session) -> list[CategoryOut]:
    """Return a cached, serialised list of categories.

    The cache keeps detached Pydantic-compatible payloads instead of ORM
    instances so we can safely reuse them across sessions.
    """

    now = monotonic()
    entry: _CacheEntry | None = _CATEGORIES_CACHE.get(_CACHE_KEY)
    if entry and entry.expires_at > now:
        return entry.payload

    rows = (
        db.query(Category)
        .order_by(Category.parent_id.is_(None).desc(), Category.name.asc())
        .all()
    )
    payload = _serialize_categories(rows)
    _CATEGORIES_CACHE[_CACHE_KEY] = _CacheEntry(
        expires_at=now + _CACHE_TTL_SECONDS,
        payload=payload,
    )
    return payload
