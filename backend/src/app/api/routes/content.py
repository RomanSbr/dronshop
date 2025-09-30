from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.data.content_blocks import HERO_SLIDES, PROMO_BLOCKS


router = APIRouter()


@router.get('/content/hero')
def content_hero(db: Session = Depends(get_db)):
    del db
    # For now the content is static, but the dependency keeps the interface
    # ready for a future database-backed CMS.
    return HERO_SLIDES


@router.get('/content/promo')
def content_promo(db: Session = Depends(get_db)):
    del db
    return PROMO_BLOCKS
