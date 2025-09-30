from fastapi import HTTPException, Request
import time
from typing import Dict, Tuple
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# In-memory store for rate limiting (in production use Redis)
_rate_limit_store: Dict[str, Tuple[int, float]] = {}


class RateLimiter:
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window

    async def __call__(self, request: Request):
        # Get client IP
        client_ip = request.client.host
        if not client_ip:
            # Fallback to X-Forwarded-For header if behind proxy
            x_forwarded_for = request.headers.get("X-Forwarded-For")
            if x_forwarded_for:
                client_ip = x_forwarded_for.split(",")[0].strip()
            else:
                client_ip = "unknown"

        # Get endpoint path for more granular rate limiting
        endpoint = request.url.path

        # Create a unique key for this client and endpoint
        key = f"{client_ip}:{endpoint}"

        current_time = time.time()

        # Clean up old entries
        self._cleanup_old_entries(current_time)

        # Check rate limit
        if key in _rate_limit_store:
            count, last_time = _rate_limit_store[key]

            # Reset counter if time window has passed
            if current_time - last_time > self.time_window:
                count = 1
                last_time = current_time
            else:
                count += 1

            # Update store
            _rate_limit_store[key] = (count, last_time)

            # Check if limit exceeded
            if count > self.max_requests:
                logger.warning(
                    f"Rate limit exceeded for {client_ip} on {endpoint}")
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Try again in {int(self.time_window - (current_time - last_time))} seconds.",
                    headers={"Retry-After": str(self.time_window)}
                )
        else:
            # First request from this client to this endpoint
            _rate_limit_store[key] = (1, current_time)

        return True

    def _cleanup_old_entries(self, current_time: float):
        """Remove entries older than 2 * time_window to prevent memory leaks"""
        keys_to_remove = []
        for key, (_, last_time) in _rate_limit_store.items():
            if current_time - last_time > 2 * self.time_window:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            # Use pop with default to avoid KeyError under concurrency
            _rate_limit_store.pop(key, None)


"""
Tunable limits. In dev, relax limits to avoid accidental lockouts
when navigating quickly or hot-reloading.
"""

# Global rate limiter for general API endpoints
global_rate_limiter = RateLimiter(max_requests=200, time_window=60)

if settings.DEV_LOGIN_ENABLED or settings.DEV_SEED:
    # More permissive in dev
    auth_rate_limiter = RateLimiter(max_requests=100, time_window=60)
    strict_rate_limiter = RateLimiter(max_requests=200, time_window=60)
else:
    # Production-leaning defaults
    auth_rate_limiter = RateLimiter(max_requests=10, time_window=60)
    strict_rate_limiter = RateLimiter(max_requests=20, time_window=60)


async def rate_limit_middleware(request: Request, call_next):
    try:
        # Apply different rate limits based on endpoint
        if request.url.path.startswith("/api/auth"):
            await auth_rate_limiter(request)
        elif request.url.path.startswith("/api/admin"):
            await strict_rate_limiter(request)
        else:
            await global_rate_limiter(request)
    except HTTPException:
        # Re-raise rate limit exceptions
        raise
    except Exception as e:
        # Log other errors but don't block the request
        logger.error(f"Rate limiting error: {str(e)}")

    response = await call_next(request)
    return response
