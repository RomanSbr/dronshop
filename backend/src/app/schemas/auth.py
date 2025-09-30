from pydantic import BaseModel
from pydantic import field_validator


class RequestCodeIn(BaseModel):
    phone: str


class VerifyCodeIn(BaseModel):
    phone: str
    verificationCode: str


class TokenPair(BaseModel):
    accessToken: str
    refreshToken: str


class MeOut(BaseModel):
    id: int
    phone: str
    name: str | None = None
    email: str | None = None
    roles: list[str]

class RegisterIn(BaseModel):
    contact_type: str  # 'email' or 'phone'
    contact_value: str
    password: str
    password_confirm: str

    @field_validator('contact_type')
    @classmethod
    def validate_type(cls, v):
        v = (v or '').lower()
        if v not in {'email', 'phone'}:
            raise ValueError('contact_type must be email or phone')
        return v

    @field_validator('password_confirm')
    @classmethod
    def validate_confirm(cls, v, info):
        data = info.data
        if 'password' in data and v != data['password']:
            raise ValueError('Passwords do not match')
        return v


class LoginPasswordIn(BaseModel):
    contact_type: str  # 'email' or 'phone'
    contact_value: str
    password: str


class AdminUserOut(BaseModel):
    id: int
    phone: str | None = None
    email: str | None = None
    name: str | None = None
    roles: list[str]
    is_blocked: bool
    is_verified: bool
    created_at: str | None = None


