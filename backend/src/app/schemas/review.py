from pydantic import BaseModel
from datetime import datetime


class ReviewBase(BaseModel):
    product_id: int
    name: str
    email: str
    title: str
    content: str
    pros: str | None = None
    cons: str | None = None
    rating: int


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    title: str | None = None
    content: str | None = None
    pros: str | None = None
    cons: str | None = None
    rating: int | None = None
    approved: bool | None = None


class ReviewOut(ReviewBase):
    id: int
    user_id: int | None = None
    helpful_count: int
    approved: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewAdminOut(ReviewOut):
    email: str
