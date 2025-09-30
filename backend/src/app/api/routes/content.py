from fastapi import APIRouter

router = APIRouter()

@router.get('/content/hero')
def content_hero():
    return []

@router.get('/content/promo')
def content_promo():
    return []
