from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from app.api.deps import get_db, require_roles
from app.models.site_settings import SiteSetting
from app.schemas.site_settings import SiteSettingOut, SiteSettingCreate, SiteSettingUpdate, SiteSettingsDict

router = APIRouter()


@router.get("/settings", response_model=List[SiteSettingOut])
def get_all_settings(
    db: Session = Depends(get_db),
    include_private: bool = False,
    current_user: dict = Depends(require_roles("admin")),
):
    """
    Получить все настройки сайта (только для администраторов)
    """
    query = db.query(SiteSetting)
    if not include_private:
        query = query.filter(SiteSetting.is_public.is_(True))

    settings = query.all()
    return settings


@router.get("/settings/public", response_model=SiteSettingsDict)
def get_public_settings(db: Session = Depends(get_db)):
    """
    Получить публичные настройки сайта (доступно всем)
    """
    settings = db.query(SiteSetting).filter(
        SiteSetting.is_public.is_(True)).all()
    return {"settings": {s.key: s.value for s in settings if s.value is not None}}


@router.get("/settings/{key}", response_model=SiteSettingOut)
def get_setting(
    key: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("admin")),
):
    """
    Получить настройку по ключу (только для администраторов)
    """
    setting = db.query(SiteSetting).filter(SiteSetting.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting


@router.post("/settings", response_model=SiteSettingOut, dependencies=[Depends(require_roles("admin"))])
def create_setting(
    setting: SiteSettingCreate,
    db: Session = Depends(get_db),
):
    """
    Создать новую настройку сайта (только для администраторов)
    """
    existing = db.query(SiteSetting).filter(
        SiteSetting.key == setting.key).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Setting with this key already exists")

    db_setting = SiteSetting(**setting.model_dump())
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting


@router.put("/settings/{key}", response_model=SiteSettingOut, dependencies=[Depends(require_roles("admin"))])
def update_setting(
    key: str,
    setting: SiteSettingUpdate,
    db: Session = Depends(get_db),
):
    """
    Обновить настройку сайта (только для администраторов)
    """
    db_setting = db.query(SiteSetting).filter(SiteSetting.key == key).first()
    if not db_setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    update_data = setting.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_setting, field, value)

    db.commit()
    db.refresh(db_setting)
    return db_setting


@router.delete("/settings/{key}", dependencies=[Depends(require_roles("admin"))])
def delete_setting(
    key: str,
    db: Session = Depends(get_db),
):
    """
    Удалить настройку сайта (только для администраторов)
    """
    db_setting = db.query(SiteSetting).filter(SiteSetting.key == key).first()
    if not db_setting:
        raise HTTPException(status_code=404, detail="Setting not found")

    db.delete(db_setting)
    db.commit()
    return {"success": True}


@router.post("/settings/batch", response_model=SiteSettingsDict, dependencies=[Depends(require_roles("admin"))])
def update_settings_batch(
    settings: Dict[str, str],
    db: Session = Depends(get_db),
):
    """
    Обновить несколько настроек сайта одновременно (только для администраторов)
    """
    for key, value in settings.items():
        setting = db.query(SiteSetting).filter(SiteSetting.key == key).first()
        if setting:
            setting.value = value
        else:
            db.add(SiteSetting(key=key, value=value))

    db.commit()
    return {"settings": settings}
