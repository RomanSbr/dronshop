from datetime import datetime
from pydantic import BaseModel


class OrderCustomer(BaseModel):
    email: str
    firstName: str
    lastName: str
    phone: str


class OrderShipping(BaseModel):
    method: str
    address: str | None = None
    city: str | None = None
    postalCode: str | None = None
    comment: str | None = None


class OrderPayment(BaseModel):
    method: str


class OrderItemIn(BaseModel):
    productId: int
    quantity: int
    price: int


class OrderCreate(BaseModel):
    customer: OrderCustomer
    shipping: OrderShipping
    payment: OrderPayment
    items: list[OrderItemIn]
    totalAmount: int


class OrderItemOut(BaseModel):
    productId: int
    productName: str
    quantity: int
    unitPrice: int
    totalPrice: int


class OrderOut(BaseModel):
    id: int
    orderNumber: str
    status: str
    totalAmount: int
    createdAt: datetime
    items: list[OrderItemOut]


class OrderAdminOut(OrderOut):
    customer: OrderCustomer
    shipping: OrderShipping
    payment: OrderPayment


class OrderSummaryOut(BaseModel):
    id: int
    orderNumber: str
    status: str
    totalAmount: int
    createdAt: datetime
    itemsCount: int
