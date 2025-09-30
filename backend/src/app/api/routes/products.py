from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.product import Category, Inventory, Product
from app.schemas.product import CategoryOut, ProductOut, ProductsResponse
from app.services.product_media import products_to_out


router = APIRouter()


@router.get("/products", response_model=ProductsResponse)
def list_products(
    db: Session = Depends(get_db),
    category: int | None = None,
    q: str | None = None,
    sort: str | None = Query(
        None, pattern="^(price|name|created_at)(:(asc|desc))?$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    price_min: int | None = Query(None, ge=0),
    price_max: int | None = Query(None, ge=0),
    in_stock: bool = False,
):
    if price_min is not None and price_max is not None and price_min > price_max:
        price_min, price_max = price_max, price_min

    base_query = db.query(Product).filter(Product.active.is_(True))

    if category:
        base_query = base_query.filter(Product.category_id == category)
    if q:
        like = f"%{q}%"
        base_query = base_query.filter(Product.name.ilike(like))
    if price_min is not None:
        base_query = base_query.filter(Product.price >= price_min)
    if price_max is not None:
        base_query = base_query.filter(Product.price <= price_max)
    if in_stock:
        availability = Inventory.current_stock - Inventory.reserved_stock
        base_query = base_query.join(Inventory).filter(availability > 0)

    total = base_query.with_entities(func.count(
        func.distinct(Product.id))).scalar() or 0

    if sort:
        key, _, direction = sort.partition(":")
        direction = direction or "asc"
        column = getattr(Product, key)
        sorted_query = base_query.order_by(
            column.desc() if direction == "desc" else column.asc())
    else:
        sorted_query = base_query.order_by(Product.created_at.desc())

    offset = (page - 1) * page_size
    rows = sorted_query.offset(offset).limit(page_size).all()

    items = products_to_out(db, rows)

    total_pages = ceil(total / page_size) if page_size else 1
    has_next = page < total_pages
    has_prev = page > 1 and total > 0

    return {
        "items": items,
        "meta": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": has_next,
            "has_prev": has_prev,
        },
    }


@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product or not product.active:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_to_out(db, [product])[0]


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    rows = db.query(Category).all()
    return [CategoryOut(id=c.id, slug=c.slug, name=c.name, parent_id=c.parent_id) for c in rows]
