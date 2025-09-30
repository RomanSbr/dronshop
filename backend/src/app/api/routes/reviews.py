from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, require_roles, get_current_user_id
from app.models.review import Review
from app.models.product import Product
from app.schemas.review import ReviewCreate, ReviewOut, ReviewUpdate, ReviewAdminOut

router = APIRouter()


@router.post("/products/{product_id}/reviews", response_model=ReviewOut)
def create_review(
    product_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user_id: int | None = Depends(get_current_user_id),
):
    # Проверяем существование продукта
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Создаем отзыв
    db_review = Review(
        product_id=product_id,
        user_id=current_user_id,
        name=review.name,
        email=review.email,
        title=review.title,
        content=review.content,
        pros=review.pros,
        cons=review.cons,
        rating=review.rating,
        helpful_count=0,
        approved=False,  # Отзывы требуют одобрения администратором
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/products/{product_id}/reviews", response_model=List[ReviewOut])
def get_product_reviews(
    product_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    # Получаем только одобренные отзывы для публичного API
    reviews = db.query(Review).filter(
        Review.product_id == product_id,
        Review.approved.is_(True)
    ).offset(skip).limit(limit).all()
    return reviews


@router.post("/reviews/{review_id}/helpful")
def mark_review_helpful(
    review_id: int,
    helpful: bool = True,
    db: Session = Depends(get_db),
):
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if helpful:
        review.helpful_count += 1
    else:
        review.helpful_count = max(0, review.helpful_count - 1)

    db.commit()
    return {"success": True, "helpful_count": review.helpful_count}


# Админские эндпоинты

@router.get("/admin/reviews", response_model=List[ReviewAdminOut], dependencies=[Depends(require_roles("admin"))])
def get_all_reviews(
    db: Session = Depends(get_db),
    approved: bool | None = None,
    product_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(Review)

    if approved is not None:
        query = query.filter(Review.approved == approved)

    if product_id is not None:
        query = query.filter(Review.product_id == product_id)

    reviews = query.order_by(Review.created_at.desc()
                             ).offset(skip).limit(limit).all()
    return reviews


@router.put("/admin/reviews/{review_id}", response_model=ReviewAdminOut, dependencies=[Depends(require_roles("admin"))])
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    db: Session = Depends(get_db),
):
    db_review = db.get(Review, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Обновляем только предоставленные поля
    update_data = review_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review


@router.delete("/admin/reviews/{review_id}", dependencies=[Depends(require_roles("admin"))])
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    db_review = db.get(Review, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(db_review)
    db.commit()
    return {"success": True}


@router.post("/admin/reviews/{review_id}/approve", response_model=ReviewAdminOut, dependencies=[Depends(require_roles("admin"))])
def approve_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    db_review = db.get(Review, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db_review.approved = True
    db.commit()
    db.refresh(db_review)
    return db_review


@router.post("/admin/reviews/{review_id}/reject", response_model=ReviewAdminOut, dependencies=[Depends(require_roles("admin"))])
def reject_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    db_review = db.get(Review, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db_review.approved = False
    db.commit()
    db.refresh(db_review)
    return db_review
