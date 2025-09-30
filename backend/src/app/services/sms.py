from time import time
from app.core.config import settings
from secrets import randbelow


_store: dict[str, tuple[str, float]] = {}


def _gen_code() -> str:
    n = settings.SMS_CODE_LENGTH
    max_val = 10 ** n
    return str(randbelow(max_val)).zfill(n)


def send_code(phone: str) -> str:
    code = _gen_code()
    expires_at = time() + settings.SMS_CODE_TTL_SECONDS
    _store[phone] = (code, expires_at)
    # В реальном мире — отправка через провайдера
    return code  # возвращаем для эмуляции/логирования


def verify_code(phone: str, provided: str) -> bool:
    if phone not in _store:
        return False
    code, expires_at = _store[phone]
    if time() > expires_at:
        del _store[phone]
        return False
    if code != provided:
        return False
    del _store[phone]
    return True
