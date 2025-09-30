from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, select
import shutil
import uuid
from pathlib import Path

from app.api.deps import get_db, require_roles
from app.models.product import Category, Product, Inventory, ProductImage
from app.models.user import User, user_roles_names
from app.models.role import Role
from app.schemas.auth import AdminUserOut
from app.schemas.product import (
    ProductIn,
    ProductOut,
    InventoryOut,
    ProductUpdate,
    InventoryUpdate,
    BulkInventoryUpdate,
    CategoryIn,
    CategoryOut,
    CategoryUpdate,
)
from app.core.config import settings
from app.services.product_media import products_to_out


router = APIRouter()


def _category_to_out(category: Category) -> CategoryOut:
    return CategoryOut(
        id=category.id,
        slug=category.slug,
        name=category.name,
        parent_id=category.parent_id,
    )


def _ensure_parent_valid(category: Category | None, parent_id: int | None, db: Session) -> None:
    if parent_id is None:
        return
    parent = db.get(Category, parent_id)
    if not parent:
        raise HTTPException(
            status_code=404, detail="Parent category not found")
    if category and parent.id == category.id:
        raise HTTPException(
            status_code=400, detail="Category cannot be its own parent")
    if category:
        ancestor = parent
        visited: set[int] = set()
        while ancestor:
            if ancestor.id == category.id:
                raise HTTPException(
                    status_code=400, detail="Parent category creates a cycle")
            if ancestor.parent_id is None:
                break
            if ancestor.parent_id in visited:
                break
            visited.add(ancestor.id)
            ancestor = db.get(Category, ancestor.parent_id)


@router.get("/categories", response_model=list[CategoryOut], dependencies=[Depends(require_roles("admin"))])
def admin_list_categories(db: Session = Depends(get_db)):
    rows = db.query(Category).order_by(Category.name.asc()).all()
    return [_category_to_out(row) for row in rows]


@router.get("/categories/{category_id}", response_model=CategoryOut, dependencies=[Depends(require_roles("admin"))])
def admin_get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return _category_to_out(category)


@router.post("/categories", response_model=CategoryOut, dependencies=[Depends(require_roles("admin"))])
def admin_create_category(payload: CategoryIn, db: Session = Depends(get_db)):
    existing = db.query(Category).filter(Category.slug == payload.slug).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Category with this slug already exists")
    _ensure_parent_valid(None, payload.parent_id, db)
    category = Category(slug=payload.slug, name=payload.name,
                        parent_id=payload.parent_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return _category_to_out(category)


@router.put("/categories/{category_id}", response_model=CategoryOut, dependencies=[Depends(require_roles("admin"))])
def admin_update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    update_data = payload.model_dump(exclude_unset=True)
    if "slug" in update_data and update_data["slug"] != category.slug:
        conflict = db.query(Category).filter(
            Category.slug == update_data["slug"], Category.id != category.id).first()
        if conflict:
            raise HTTPException(
                status_code=400, detail="Category with this slug already exists")
    if "parent_id" in update_data:
        _ensure_parent_valid(category, update_data["parent_id"], db)
    for field, value in update_data.items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return _category_to_out(category)


@router.delete("/categories/{category_id}", dependencies=[Depends(require_roles("admin"))])
def admin_delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category. If there are child categories, reparent them to the
    deleted category's parent. If there are products in the category, detach
    them by setting product.category_id = NULL so deletion can proceed.
    """
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Reparent children to this category's parent (may be NULL)
    children = db.query(Category).filter(Category.parent_id == category_id).all()
    for child in children:
        child.parent_id = category.parent_id

    # Detach products from this category
    products = db.query(Product).filter(Product.category_id == category_id).all()
    for p in products:
        p.category_id = None

    db.delete(category)
    db.commit()
    return {"success": True}


@router.post("/products", response_model=ProductOut, dependencies=[Depends(require_roles("admin"))])
def create_product(payload: ProductIn, db: Session = Depends(get_db)):
    p = Product(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        category_id=payload.category_id,
        active=payload.active,
    )
    db.add(p)
    db.flush()
    inv = Inventory(product_id=p.id, current_stock=0, reserved_stock=0)
    db.add(inv)
    db.commit()
    db.refresh(p)
    return products_to_out(db, [p])[0]


@router.get("/products", response_model=list[ProductOut], dependencies=[Depends(require_roles("admin"))])
def admin_list_products(
    db: Session = Depends(get_db),
    category: int | None = None,
    q: str | None = None,
    active: bool | None = None,
    sort: str | None = None,
    page: int = 1,
    page_size: int = 100,
):
    stmt = select(Product)
    if category:
        stmt = stmt.where(Product.category_id == category)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(Product.name.ilike(like))
    if active is not None:
        stmt = stmt.where(Product.active == active)
    if sort:
        key, _, direction = sort.partition(":")
        direction = direction or "asc"
        if hasattr(Product, key):
            col = getattr(Product, key)
            stmt = stmt.order_by(col.desc() if direction ==
                                 "desc" else col.asc())
    else:
        stmt = stmt.order_by(Product.created_at.desc())

    offset = max(0, (page - 1) * page_size)
    stmt = stmt.offset(offset).limit(page_size)
    rows = db.execute(stmt).scalars().all()
    return products_to_out(db, rows)


@router.get("/inventory", response_model=list[InventoryOut], dependencies=[Depends(require_roles("admin"))])
def get_inventory(db: Session = Depends(get_db)):
    stmt = select(Product, Inventory).join(
        Inventory, Inventory.product_id == Product.id, isouter=True)
    rows = db.execute(stmt).all()
    out: list[InventoryOut] = []
    for p, inv in rows:
        current = inv.current_stock if inv else 0
        reserved = inv.reserved_stock if inv else 0
        out.append(
            InventoryOut(
                productId=p.id,
                productName=p.name,
                currentStock=current,
                reservedStock=reserved,
                availableStock=max(0, current - reserved),
            )
        )
    return out


@router.put("/inventory/{product_id}", dependencies=[Depends(require_roles("admin"))])
def update_inventory(
    product_id: int,
    inventory: InventoryUpdate,
    db: Session = Depends(get_db),
):
    """
    Р С›Р В±Р Р…Р С•Р Р†Р В»Р ВµР Р…Р С‘Р Вµ Р С•РЎРѓРЎвЂљР В°РЎвЂљР С”Р С•Р Р† РЎвЂљР С•Р Р†Р В°РЎР‚Р В°
    """
    # Р СџРЎР‚Р С•Р Р†Р ВµРЎР‚РЎРЏР ВµР С РЎРѓРЎС“РЎвЂ°Р ВµРЎРѓРЎвЂљР Р†Р С•Р Р†Р В°Р Р…Р С‘Р Вµ РЎвЂљР С•Р Р†Р В°РЎР‚Р В°
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Р СџР С•Р В»РЎС“РЎвЂЎР В°Р ВµР С Р В·Р В°Р С—Р С‘РЎРѓРЎРЉ Р С‘Р Р…Р Р†Р ВµР Р…РЎвЂљР В°РЎР‚РЎРЏ Р С‘Р В»Р С‘ РЎРѓР С•Р В·Р Т‘Р В°Р ВµР С Р Р…Р С•Р Р†РЎС“РЎР‹
    inventory_record = db.query(Inventory).filter(
        Inventory.product_id == product_id).first()
    if not inventory_record:
        inventory_record = Inventory(
            product_id=product_id, current_stock=0, reserved_stock=0)
        db.add(inventory_record)

    # Р С›Р В±Р Р…Р С•Р Р†Р В»РЎРЏР ВµР С Р С•РЎРѓРЎвЂљР В°РЎвЂљР С•Р С”
    inventory_record.current_stock = inventory.current_stock

    db.commit()

    return {
        "success": True,
        "productId": product_id,
        "currentStock": inventory_record.current_stock,
        "reservedStock": inventory_record.reserved_stock,
        "availableStock": max(0, inventory_record.current_stock - inventory_record.reserved_stock)
    }


@router.post("/inventory/bulk-update", dependencies=[Depends(require_roles("admin"))])
def bulk_update_inventory(
    update_data: BulkInventoryUpdate,
    db: Session = Depends(get_db),
):
    """
    Р СљР В°РЎРѓРЎРѓР С•Р Р†Р С•Р Вµ Р С•Р В±Р Р…Р С•Р Р†Р В»Р ВµР Р…Р С‘Р Вµ Р С•РЎРѓРЎвЂљР В°РЎвЂљР С”Р С•Р Р† РЎвЂљР С•Р Р†Р В°РЎР‚Р С•Р Р†
    """
    # Р В¤Р С•РЎР‚Р СР С‘РЎР‚РЎС“Р ВµР С Р В·Р В°Р С—РЎР‚Р С•РЎРѓ Р Р† Р В·Р В°Р Р†Р С‘РЎРѓР С‘Р СР С•РЎРѓРЎвЂљР С‘ Р С•РЎвЂљ Р С”Р В°РЎвЂљР ВµР С–Р С•РЎР‚Р С‘Р С‘
    query = db.query(Inventory).join(
        Product, Product.id == Inventory.product_id)

    if update_data.category_id is not None:
        query = query.filter(Product.category_id == update_data.category_id)

    inventory_records = query.all()

    # Р С›Р В±Р Р…Р С•Р Р†Р В»РЎРЏР ВµР С Р С•РЎРѓРЎвЂљР В°РЎвЂљР С”Р С‘ Р Р† Р В·Р В°Р Р†Р С‘РЎРѓР С‘Р СР С•РЎРѓРЎвЂљР С‘ Р С•РЎвЂљ Р Р†РЎвЂ№Р В±РЎР‚Р В°Р Р…Р Р…Р С•Р С–Р С• Р Т‘Р ВµР в„–РЎРѓРЎвЂљР Р†Р С‘РЎРЏ
    for record in inventory_records:
        if update_data.action == "set":
            record.current_stock = update_data.quantity
        elif update_data.action == "add":
            record.current_stock += update_data.quantity
        elif update_data.action == "subtract":
            record.current_stock = max(
                0, record.current_stock - update_data.quantity)

    db.commit()

    return {"success": True, "updated_count": len(inventory_records)}


@router.get("/products/{product_id}", response_model=ProductOut, dependencies=[Depends(require_roles("admin"))])
def get_product_admin(
    product_id: int,
    db: Session = Depends(get_db),
):
    """
    Р’РѕР·РІСЂР°С‰Р°РµС‚ РґРµС‚Р°Р»Рё С‚РѕРІР°СЂР° РґР»СЏ Р°РґРјРёРЅРёСЃС‚СЂР°С‚РёРІРЅРѕР№ РїР°РЅРµР»Рё.
    """
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_to_out(db, [product])[0]


@router.put("/products/{product_id}", response_model=ProductOut, dependencies=[Depends(require_roles("admin"))])
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
):
    """
    РћР±РЅРѕРІР»СЏРµС‚ РїРѕР»СЏ С‚РѕРІР°СЂР°.
    """
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return products_to_out(db, [product])[0]


@router.delete("/products/{product_id}", dependencies=[Depends(require_roles("admin"))])
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a product along with its images and inventory record. Images are
    removed from disk if they exist.
    """
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Delete images from filesystem and DB
    images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
    for img in images:
        # Convert stored URL to filesystem path under uploads dir
        relative = Path(img.url.lstrip("/"))
        if relative.parts and relative.parts[0] == "uploads":
            relative = Path(*relative.parts[1:])
        file_path = Path(settings.UPLOADS_DIR) / relative
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception:
            # Ignore filesystem errors during deletion
            pass
        db.delete(img)

    # Delete inventory record if present
    inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if inv:
        db.delete(inv)

    # Finally delete the product
    db.delete(product)
    db.commit()

    # Try removing now-empty upload directory
    try:
        uploads_dir = Path(settings.UPLOADS_DIR) / "products" / str(product_id)
        if uploads_dir.exists():
            uploads_dir.rmdir()
    except Exception:
        pass

    return {"success": True}


@router.post("/products/{product_id}/upload-image", dependencies=[Depends(require_roles("admin"))])
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Р—Р°РіСЂСѓР¶Р°РµС‚ РёР·РѕР±СЂР°Р¶РµРЅРёРµ С‚РѕРІР°СЂР° Рё С„РёРєСЃРёСЂСѓРµС‚ РµРіРѕ РІ Р±Р°Р·Рµ.
    """
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    extension = Path(file.filename or "").suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        extension = ".jpg"

    relative_folder = Path("products") / str(product_id)
    upload_dir = Path(settings.UPLOADS_DIR) / relative_folder
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{uuid.uuid4().hex}{extension}"
    file_path = upload_dir / file_name

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    current_sort = db.query(func.max(ProductImage.sort)).filter(
        ProductImage.product_id == product_id).scalar() or 0
    relative_path = relative_folder / file_name
    image_url = f"/uploads/{relative_path.as_posix()}"
    image = ProductImage(product_id=product_id,
                         url=image_url, sort=current_sort + 1)
    db.add(image)
    db.commit()
    db.refresh(image)

    return {
        "success": True,
        "image_url": image.url,
        "image": {"id": image.id, "url": image.url, "sort": image.sort},
    }


@router.delete("/products/{product_id}/images/{image_id}", dependencies=[Depends(require_roles("admin"))])
def delete_product_image(
    product_id: int,
    image_id: int,
    db: Session = Depends(get_db),
):
    """
    РЈРґР°Р»СЏРµС‚ РёР·РѕР±СЂР°Р¶РµРЅРёРµ С‚РѕРІР°СЂР° РІРјРµСЃС‚Рµ СЃ С„Р°Р№Р»РѕРј.
    """
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    image = (
        db.query(ProductImage)
        .filter(ProductImage.id == image_id, ProductImage.product_id == product_id)
        .first()
    )
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    relative = Path(image.url.lstrip("/"))
    if relative.parts and relative.parts[0] == "uploads":
        relative = Path(*relative.parts[1:])
    file_path = Path(settings.UPLOADS_DIR) / relative
    if file_path.exists():
        file_path.unlink()

    db.delete(image)
    db.commit()
    return {"success": True}

# ---------- Users management ----------

@router.get("/users", response_model=list[AdminUserOut], dependencies=[Depends(require_roles("admin"))])
def admin_list_users(db: Session = Depends(get_db)):
    rows = db.query(User).order_by(User.created_at.desc()).all()
    out: list[AdminUserOut] = []
    for u in rows:
        out.append(AdminUserOut(
            id=u.id,
            phone=u.phone,
            email=u.email,
            name=u.name,
            roles=user_roles_names(u),
            is_blocked=getattr(u, 'is_blocked', False),
            is_verified=getattr(u, 'is_verified', False),
            created_at=str(getattr(u, 'created_at', '')),
        ))
    return out

@router.patch("/users/{user_id}", dependencies=[Depends(require_roles("admin"))])
def admin_update_user(user_id: int, action: str, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    action = (action or '').lower()
    if action == 'block':
        user.is_blocked = True
    elif action == 'unblock':
        user.is_blocked = False
    elif action == 'make_admin':
        role = db.query(Role).filter(Role.name == 'admin').first() or Role(name='admin')
        if role.id is None:
            db.add(role)
            db.flush()
        if role not in user.roles_rel:
            user.roles_rel.append(role)
        user.roles = ','.join(user_roles_names(user))
    elif action == 'remove_admin':
        user.roles_rel = [r for r in user.roles_rel if r.name != 'admin']
        user.roles = ','.join(user_roles_names(user))
    else:
        raise HTTPException(status_code=400, detail="Unsupported action")
    db.commit()
    return {"success": True}

@router.delete("/users/{user_id}", dependencies=[Depends(require_roles("admin"))])
def admin_delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"success": True}






