from pydantic import BaseModel
from typing import Optional


class SiteSettingBase(BaseModel):
    key: str
    value: Optional[str] = None
    description: Optional[str] = None
    is_public: bool = True


class SiteSettingCreate(SiteSettingBase):
    pass


class SiteSettingUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None


class SiteSettingOut(SiteSettingBase):
    class Config:
        from_attributes = True


class SiteSettingsDict(BaseModel):
    settings: dict[str, str]
