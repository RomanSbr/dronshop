from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes.auth import router as auth_router
from app.api.routes.products import router as products_router
from app.api.routes.admin import router as admin_router
from app.api.routes.reviews import router as reviews_router
from app.api.routes.site_settings import router as site_settings_router
from app.api.routes.orders import router as orders_router
from app.api.routes.content import router as content_router
from app.core.config import settings
from app.data.demo_catalog import CATEGORIES, PRODUCTS
from app.db.base import Base
from app.db.session import SessionLocal, engine
from sqlalchemy import text
from app.middleware.rate_limit import rate_limit_middleware
from app.models.product import Category, Inventory, Product, ProductImage
from app.models.site_settings import SiteSetting
from app.models.user import User
from app.models.role import Role

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    Base.metadata.create_all(bind=engine)
    # Lightweight column migration for users table (SQLite-friendly)
    with engine.connect() as conn:
        try:
            cols = {row[1] for row in conn.exec_driver_sql("PRAGMA table_info('users')").fetchall()}
            if 'password_hash' not in cols:
                conn.exec_driver_sql("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)")
            if 'is_verified' not in cols:
                conn.exec_driver_sql("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT 0")
            if 'is_blocked' not in cols:
                conn.exec_driver_sql("ALTER TABLE users ADD COLUMN is_blocked BOOLEAN DEFAULT 0")
        except Exception:
            pass
    db = SessionLocal()
    try:
        if db.query(SiteSetting).count() == 0:
            default_settings = [
                SiteSetting(key="site_name", value="DronShop",
                            description="Site name", is_public=True),
                SiteSetting(key="site_description", value="FPV/RC shop demo",
                            description="Site description", is_public=True),
                SiteSetting(key="contact_email", value="info@dronshop.ru",
                            description="Contact email", is_public=True),
                SiteSetting(key="contact_phone", value="+7 (999) 000-00-00",
                            description="Contact phone", is_public=True),
            ]
            for setting in default_settings:
                db.add(setting)
            db.commit()

        if db.query(Category).count() == 0:
            for category in CATEGORIES:
                db.add(Category(slug=category["slug"], name=category["name"]))
            db.commit()

        # Only seed demo catalog when explicitly enabled AND no products exist yet.
        # This prevents accidental overwriting of imported/custom data.
        if settings.DEV_SEED and (db.query(Product).count() == 0):
            # Ensure base roles exist
            role_admin = db.query(Role).filter(Role.name == "admin").first() or Role(name="admin")
            role_buyer = db.query(Role).filter(Role.name == "buyer").first() or Role(name="buyer")
            db.add(role_admin)
            db.add(role_buyer)
            db.commit()

            users_seed = [
                ("+70000000001", ["buyer", "admin"], "admin"),
                ("+70000000002", ["buyer"], "buyer"),
            ]
            for phone, roles, name in users_seed:
                existing = db.query(User).filter(User.phone == phone).first()
                if not existing:
                    user = User(phone=phone, roles=",".join(roles), name=name)
                    rels = db.query(Role).filter(Role.name.in_(roles)).all()
                    user.roles_rel = rels
                    db.add(user)
            db.commit()

            categories = db.query(Category).all()
            slug_to_id = {category.slug: category.id for category in categories}

            for item in PRODUCTS:
                category_id = slug_to_id.get(item["category"])
                if not category_id:
                    continue
                product = Product(
                    name=item["name"],
                    description=item["description"],
                    price=item["price"],
                    category_id=category_id,
                    active=True,
                )
                db.add(product)
                db.flush()
                db.add(Inventory(
                    product_id=product.id,
                    current_stock=item.get("stock", 20),
                    reserved_stock=item.get("reserved", 0),
                ))
            db.commit()
        yield
    finally:
        db.close()

app = FastAPI(lifespan=lifespan, title="Dronshop API", version="0.1.0")

# Add rate limiting middleware
app.middleware("http")(rate_limit_middleware)

origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(products_router, prefix="/api", tags=["products"])
app.include_router(orders_router, prefix="/api", tags=["orders"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(reviews_router, prefix="/api", tags=["reviews"])
app.include_router(site_settings_router, prefix="/api", tags=["settings"])
app.include_router(content_router, prefix="/api", tags=["content"])

@app.get("/api/health")
def health():
    return {"status": "ok"}




# Serve static files from uploads directory
app.mount("/uploads", StaticFiles(directory="/app/uploads_temp"), name="uploads")
