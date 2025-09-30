from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional

from app.core.security import decode_token
from app.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


bearer = HTTPBearer(auto_error=False)


def get_current_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer)) -> dict:
    if creds is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = decode_token(creds.credentials)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Token validation error: {str(e)}")


def require_roles(*required_roles: str):
    def checker(payload: dict = Depends(get_current_user)):
        roles = payload.get("roles") or []
        # Ensure roles is a list
        if isinstance(roles, str):
            roles = [r.strip() for r in roles.split(",") if r.strip()]
        elif not isinstance(roles, list):
            roles = []
        
        if not any(r in roles for r in required_roles):
            raise HTTPException(status_code=403, detail="Forbidden")
        return payload
    return checker


def get_current_user_id(creds: HTTPAuthorizationCredentials | None = Depends(bearer)) -> Optional[int]:
    """
    Получает ID текущего пользователя из токена, но не вызывает ошибку, если токен отсутствует.
    Возвращает None, если пользователь не аутентифицирован.
    """
    if creds is None:
        return None
    try:
        payload = decode_token(creds.credentials)
        user_id = payload.get("sub")
        if user_id:
            return int(user_id)
        return None
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
    except Exception as e:
        # Логируем ошибку, но не прерываем выполнение
        import logging
        logging.warning(f"Unexpected error in get_current_user_id: {str(e)}")
        return None
