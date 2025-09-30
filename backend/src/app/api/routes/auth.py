import logging

import jwt
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.models.role import Role
from app.models.user import User, user_roles_names
from app.schemas.auth import (
    LoginPasswordIn,
    MeOut,
    RegisterIn,
    RequestCodeIn,
    TokenPair,
    VerifyCodeIn,
)
from app.services.sms import send_code, verify_code
from passlib.hash import bcrypt

from app.core.config import settings


router = APIRouter()
logger = logging.getLogger(__name__)


def _ensure_role(db: Session, name: str) -> Role:
    role = db.query(Role).filter(Role.name == name).first()
    if role:
        return role

    role = Role(name=name)
    db.add(role)
    db.flush()
    return role


@router.post("/request-code")
def request_code(payload: RequestCodeIn):
    code = send_code(payload.phone)
    return {"sent": True, "debugCode": code}


@router.post("/register", response_model=TokenPair)
def register(payload: VerifyCodeIn, db: Session = Depends(get_db)):
    if not verify_code(payload.phone, payload.verificationCode):
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    user = db.query(User).filter(User.phone == payload.phone).first()
    if not user:
        user = User(phone=payload.phone, roles="buyer")
        buyer_role = _ensure_role(db, "buyer")
        user.roles_rel.append(buyer_role)
        db.add(user)
        db.commit()
        db.refresh(user)
    access = create_access_token(str(user.id), roles=user_roles_names(user))
    refresh = create_refresh_token(str(user.id))
    return {"accessToken": access, "refreshToken": refresh}


@router.post("/login", response_model=TokenPair)
def login(payload: VerifyCodeIn, db: Session = Depends(get_db)):
    if not verify_code(payload.phone, payload.verificationCode):
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    user = db.query(User).filter(User.phone == payload.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    access = create_access_token(str(user.id), roles=user_roles_names(user))
    refresh = create_refresh_token(str(user.id))
    return {"accessToken": access, "refreshToken": refresh}


@router.post("/refresh", response_model=TokenPair)
def refresh_tokens(refreshToken: str, db: Session = Depends(get_db)):
    try:
        payload = decode_token(refreshToken)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")
        user_id = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    access = create_access_token(str(user.id), roles=user_roles_names(user))
    new_refresh = create_refresh_token(str(user.id))
    return {"accessToken": access, "refreshToken": new_refresh}


@router.get("/me", response_model=MeOut)
def me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = int(current_user.get("sub"))
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return MeOut(id=user.id, phone=user.phone, name=user.name, email=user.email, roles=user_roles_names(user))


@router.post("/register-password", response_model=TokenPair)
def register_password(payload: RegisterIn, db: Session = Depends(get_db)):
    ct = payload.contact_type.lower()
    cv = payload.contact_value.strip()
    if len(payload.password) < 8:
        raise HTTPException(status_code=400, detail="Password too short")
    # uniqueness check
    if ct == 'phone':
        exists = db.query(User).filter(User.phone == cv).first()
        if exists:
            raise HTTPException(status_code=400, detail="Phone already registered")
    else:
        exists = db.query(User).filter(User.email == cv).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email already registered")

    buyer_role = _ensure_role(db, "buyer")

    phone_value = cv if ct == 'phone' else f"email:{abs(hash(cv))%10**10}"
    user = User(phone=phone_value, email=cv if ct == 'email' else None, roles="buyer")
    user.roles_rel.append(buyer_role)
    user.password_hash = bcrypt.hash(payload.password)
    user.is_verified = True
    db.add(user)
    db.commit()
    db.refresh(user)

    access = create_access_token(str(user.id), roles=user_roles_names(user))
    refresh = create_refresh_token(str(user.id))
    return {"accessToken": access, "refreshToken": refresh}


@router.post("/login-password", response_model=TokenPair)
def login_password(payload: LoginPasswordIn, db: Session = Depends(get_db)):
    ct = payload.contact_type.lower()
    cv = payload.contact_value.strip()
    user = None
    if ct == 'phone':
        user = db.query(User).filter(User.phone == cv).first()
    else:
        user = db.query(User).filter(User.email == cv).first()
    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    try:
        if not bcrypt.verify(payload.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except ValueError as e:
        # Handle invalid bcrypt hash format
        logger.error(f"Invalid bcrypt hash for user {user.id}: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if getattr(user, 'is_blocked', False):
        raise HTTPException(status_code=403, detail="User is blocked")
    access = create_access_token(str(user.id), roles=user_roles_names(user))
    refresh = create_refresh_token(str(user.id))
    return {"accessToken": access, "refreshToken": refresh}


@router.post("/dev-login", response_model=TokenPair)
def dev_login(
    login: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db),
):
    # Allow dev login when explicitly enabled or when seeding demo data
    if not (settings.DEV_LOGIN_ENABLED or settings.DEV_SEED):
        raise HTTPException(status_code=404, detail="Not found")

    accounts = {
        "admin": {"password": "admin123", "phone": "+70000000001", "roles": ["buyer", "admin"]},
        "buyer": {"password": "buyer123", "phone": "+70000000002", "roles": ["buyer"]},
    }
    acc = accounts.get(login)
    if not acc or acc["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = db.query(User).filter(User.phone == acc["phone"]).first()
    # ensure roles exist and are assigned
    role_objs = [_ensure_role(db, rname) for rname in acc["roles"]]

    if not user:
        user = User(phone=acc["phone"], roles=",".join(acc["roles"]), name=login)
        user.roles_rel = role_objs
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.roles = ",".join(acc["roles"])  # keep legacy string in sync
        user.roles_rel = role_objs
        db.commit()

    access = create_access_token(str(user.id), roles=user_roles_names(user))
    refresh = create_refresh_token(str(user.id))
    return {"accessToken": access, "refreshToken": refresh}
