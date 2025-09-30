from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base
from app.models.role import Role, user_roles


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    phone: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(
        String(255), unique=False, nullable=True)
    roles: Mapped[str] = mapped_column(
        String(255), default="buyer")  # comma-separated roles
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow)

    # New: normalized roles via many-to-many table
    roles_rel: Mapped[list[Role]] = relationship(
        Role,
        secondary=user_roles,
        back_populates="users",
        lazy="joined",
    )


def roles_list(roles_str: str | None) -> list[str]:
    if not roles_str:
        return []
    return [r.strip() for r in roles_str.split(",") if r.strip()]


def user_roles_names(user: "User") -> list[str]:
    """Return user roles from relation if present, else fallback to comma string."""
    try:
        if user.roles_rel:
            return [r.name for r in user.roles_rel]
    except Exception:
        pass
    return roles_list(getattr(user, "roles", None))
