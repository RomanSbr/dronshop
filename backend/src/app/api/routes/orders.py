from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.api.deps import get_db, require_roles, get_current_user, get_current_user_id
from app.models.order import Order, OrderItem
from app.models.product import Inventory, Product
from app.models.user import User
from app.schemas.order import (
    OrderAdminOut,
    OrderCreate,
    OrderItemOut,
    OrderOut,
    OrderSummaryOut,
)


router = APIRouter()


def _order_to_out(order: Order) -> OrderOut:
    items = [
        OrderItemOut(
            productId=item.product_id,
            productName=item.product_name,
            quantity=item.quantity,
            unitPrice=item.unit_price,
            totalPrice=item.total_price,
        )
        for item in order.items
    ]
    return OrderOut(
        id=order.id,
        orderNumber=order.order_number,
        status=order.status,
        totalAmount=order.total_amount,
        createdAt=order.created_at,
        items=items,
    )


def _order_to_admin_out(order: Order) -> OrderAdminOut:
    base = _order_to_out(order)
    return OrderAdminOut(
        **base.model_dump(),
        customer={
            "email": order.customer_email,
            "firstName": order.customer_first_name,
            "lastName": order.customer_last_name,
            "phone": order.customer_phone,
        },
        shipping={
            "method": order.shipping_method,
            "address": order.shipping_address,
            "city": order.shipping_city,
            "postalCode": order.shipping_postal_code,
            "comment": order.shipping_comment,
        },
        payment={"method": order.payment_method},
    )


@router.post('/orders', response_model=OrderOut)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    user_id: Optional[int] = Depends(get_current_user_id),
):
    try:
        if not payload.items:
            raise HTTPException(status_code=400, detail='Cart is empty')

        # Normalize optional shipping fields (allow empty strings from UI)
        shipping_address = (payload.shipping.address or None)
        shipping_city = (payload.shipping.city or None)
        shipping_postal_code = (payload.shipping.postalCode or None)
        shipping_comment = (payload.shipping.comment or None)

        # If authenticated, prefer profile contact values over form ones
        user_obj = db.get(User, int(user_id)) if user_id else None
        customer_email = (user_obj.email if user_obj and user_obj.email else payload.customer.email)
        customer_phone = (user_obj.phone if user_obj and user_obj.phone else payload.customer.phone)

        order = Order(
            # provisional unique value to avoid unique constraint on flush
            order_number=f'ORD-TMP-{int(datetime.now().timestamp()*1000)}',
            status='pending',
            total_amount=0,
            customer_first_name=payload.customer.firstName,
            customer_last_name=payload.customer.lastName,
            customer_email=customer_email,
            customer_phone=customer_phone,
            shipping_method=payload.shipping.method,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_postal_code=shipping_postal_code,
            shipping_comment=shipping_comment,
            payment_method=payload.payment.method,
        )
        db.add(order)
        db.flush()

        order.order_number = f'ORD-{order.id:06d}'

        total_amount = 0
        for item in payload.items:
            product = db.get(Product, item.productId)
            if not product or not product.active:
                raise HTTPException(
                    status_code=400, detail=f'Product {item.productId} is unavailable')

            inventory = db.query(Inventory).filter(
                Inventory.product_id == product.id).first()
            # If there is an inventory record, validate availability; if not, do not block checkout.
            if inventory is not None:
                available = inventory.current_stock - inventory.reserved_stock
                if available < item.quantity:
                    raise HTTPException(
                        status_code=400, detail=f'Not enough stock for product {product.name}')

            unit_price = product.price
            line_total = unit_price * item.quantity
            total_amount += line_total

            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    quantity=item.quantity,
                    unit_price=unit_price,
                    total_price=line_total,
                )
            )

            if inventory is not None:
                inventory.current_stock = max(0, inventory.current_stock - item.quantity)

        order.total_amount = total_amount
        order.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(order)
        return _order_to_out(order)
    except HTTPException:
        # pass through known HTTP errors
        raise
    except Exception as e:
        import logging
        logging.exception('Order creation failed')
        raise HTTPException(status_code=500, detail=f'Order creation failed: {str(e)}')


@router.get('/admin/orders', response_model=list[OrderSummaryOut], dependencies=[Depends(require_roles('admin'))])
def admin_list_orders(db: Session = Depends(get_db)):
    rows = db.query(Order).order_by(Order.created_at.desc()).all()
    summaries: list[OrderSummaryOut] = []
    for order in rows:
        summaries.append(
            OrderSummaryOut(
                id=order.id,
                orderNumber=order.order_number,
                status=order.status,
                totalAmount=order.total_amount,
                createdAt=order.created_at,
                itemsCount=len(order.items),
            )
        )
    return summaries


@router.get('/admin/orders/{order_id}', response_model=OrderAdminOut, dependencies=[Depends(require_roles('admin'))])
def admin_get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    return _order_to_admin_out(order)


@router.patch('/admin/orders/{order_id}', response_model=OrderAdminOut, dependencies=[Depends(require_roles('admin'))])
def admin_update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    order.status = status
    order.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    return _order_to_admin_out(order)


@router.get('/orders', response_model=list[OrderSummaryOut])
def my_orders(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = int(current_user.get("sub"))
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    filters = []
    if getattr(user, 'phone', None):
        filters.append(Order.customer_phone == user.phone)
    if getattr(user, 'email', None):
        filters.append(Order.customer_email == user.email)
    if not filters:
        return []

    rows = (
        db.query(Order)
        .filter(or_(*filters))
        .order_by(Order.created_at.desc())
        .all()
    )

    summaries: list[OrderSummaryOut] = []
    for order in rows:
        summaries.append(
            OrderSummaryOut(
                id=order.id,
                orderNumber=order.order_number,
                status=order.status,
                totalAmount=order.total_amount,
                createdAt=order.created_at,
                itemsCount=len(order.items),
            )
        )
    return summaries

