from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[str] = mapped_column(
        String(32), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending")
    total_amount: Mapped[int] = mapped_column(Integer)

    customer_first_name: Mapped[str] = mapped_column(String(100))
    customer_last_name: Mapped[str] = mapped_column(String(100))
    customer_email: Mapped[str] = mapped_column(String(320))
    customer_phone: Mapped[str] = mapped_column(String(32))

    shipping_method: Mapped[str] = mapped_column(String(50))
    shipping_address: Mapped[str | None] = mapped_column(
        String(255), nullable=True)
    shipping_city: Mapped[str | None] = mapped_column(
        String(100), nullable=True)
    shipping_postal_code: Mapped[str | None] = mapped_column(
        String(20), nullable=True)
    shipping_comment: Mapped[str | None] = mapped_column(
        String(500), nullable=True)

    payment_method: Mapped[str] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey(
        "orders.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[int] = mapped_column(Integer)
    product_name: Mapped[str] = mapped_column(String(255))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[int] = mapped_column(Integer)
    total_price: Mapped[int] = mapped_column(Integer)

    order: Mapped[Order] = relationship("Order", back_populates="items")
