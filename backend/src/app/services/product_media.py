from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Iterable, Sequence
import re
import unicodedata

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.product import Product, ProductImage
from app.schemas.product import ProductImageOut, ProductOut


def _slugify(value: str) -> str:
    value = unicodedata.normalize('NFKD', value).encode(
        'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-zA-Z0-9]+', '-', value).strip('-').lower()
    return value or 'item'


def _legacy_images(name: str) -> list[str]:
    slug = _slugify(name)
    base = Path(settings.UPLOADS_DIR)
    folder = base / slug
    if not folder.exists() or not folder.is_dir():
        return []
    urls: list[str] = []
    for item in sorted(folder.iterdir()):
        if item.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp', '.gif'}:
            urls.append(f"/uploads/{slug}/{item.name}")
    return urls


def load_galleries(db: Session, product_ids: Iterable[int]) -> dict[int, list[ProductImage]]:
    ids = [int(pid) for pid in product_ids if pid is not None]
    if not ids:
        return {}
    rows = (
        db.query(ProductImage)
        .filter(ProductImage.product_id.in_(ids))
        .order_by(ProductImage.product_id.asc(), ProductImage.sort.asc(), ProductImage.id.asc())
        .all()
    )
    grouped: dict[int, list[ProductImage]] = defaultdict(list)
    for row in rows:
        grouped[row.product_id].append(row)
    return grouped


def product_to_out(product: Product, gallery: Sequence[ProductImage] | None = None) -> ProductOut:
    gallery_list = list(gallery or [])
    gallery_payload = [ProductImageOut(
        id=item.id, url=item.url, sort=item.sort) for item in gallery_list]
    urls = [item.url for item in gallery_payload]
    if not urls:
        urls = _legacy_images(product.name)
    return ProductOut(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
        active=product.active,
        image=urls[0] if urls else None,
        images=urls or None,
        gallery=gallery_payload or None,
    )


def products_to_out(db: Session, products: Sequence[Product]) -> list[ProductOut]:
    items = list(products)
    galleries = load_galleries(db, [p.id for p in items]) if items else {}
    return [product_to_out(product, galleries.get(product.id)) for product in items]
