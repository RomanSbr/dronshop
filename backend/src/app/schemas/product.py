from pydantic import BaseModel


class ProductImageOut(BaseModel):
    id: int
    url: str
    sort: int


class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: int
    category_id: int | None
    active: bool
    image: str | None = None
    images: list[str] | None = None
    gallery: list[ProductImageOut] | None = None


class ProductIn(BaseModel):
    name: str
    description: str | None = None
    price: int
    category_id: int | None = None
    active: bool = True


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    category_id: int | None = None
    active: bool | None = None


class InventoryOut(BaseModel):
    productId: int
    productName: str
    currentStock: int
    reservedStock: int
    availableStock: int


class InventoryUpdate(BaseModel):
    current_stock: int


class BulkInventoryUpdate(BaseModel):
    category_id: int | None = None
    action: str  # "set", "add", "subtract"
    quantity: int


class CategoryOut(BaseModel):
    id: int
    slug: str
    name: str
    parent_id: int | None = None


class CategoryIn(BaseModel):
    slug: str
    name: str
    parent_id: int | None = None


class CategoryUpdate(BaseModel):
    slug: str | None = None
    name: str | None = None
    parent_id: int | None = None


class ProductsMeta(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class ProductsResponse(BaseModel):
    items: list[ProductOut]
    meta: ProductsMeta
