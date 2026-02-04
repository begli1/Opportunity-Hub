# models.py
import os
import asyncio
from datetime import datetime, timezone
from sqlalchemy import Boolean
from typing import Optional
from sqlalchemy import Integer
from sqlalchemy import event

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime



# --- Engine & session ---
# PostgreSQL connection string format: postgresql+asyncpg://user:password@host:port/database
# Render automatically provides DATABASE_URL in production
# For local dev (if you have PostgreSQL): postgresql+asyncpg://postgres:password@localhost:5432/opportunityhub
# For local dev without PostgreSQL, you can temporarily use SQLite: sqlite+aiosqlite:///./app.db
DB_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/opportunityhub")

engine = create_async_engine(
    DB_URL,
    echo=os.environ.get("SQL_ECHO", "false").lower() == "true",
    pool_pre_ping=True,
    # PostgreSQL connection pool settings
    pool_size=10,
    max_overflow=20,
)

# Note: PostgreSQL has foreign keys enabled by default, no pragma needed

async_session = async_sessionmaker(engine, expire_on_commit=False)



class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(25), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    saved: Mapped[list["SavedOpportunity"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    posts: Mapped[list["Opportunity"]] = relationship(
        "Opportunity",
        back_populates="creator",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="[Opportunity.creator_user_id]",
    )



    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"

class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        UniqueConstraint("opportunity_id", "reporter_user_id", name="uq_report_once"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    # who reported
    reporter_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # what they reported
    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # reason + optional comment
    reason: Mapped[str] = mapped_column(String(40), nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # relationships for easier querying
    reporter: Mapped["User"] = relationship("User", foreign_keys=[reporter_user_id])
    opportunity: Mapped["Opportunity"] = relationship("Opportunity")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    org: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(String(80), nullable=False)


    deadline_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    deadline_text: Mapped[str] = mapped_column(String(60), nullable=False, default="")

    contact_email: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    allow_apply: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    allow_external_apply: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    external_apply_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    external_url_approved: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=None)  # None=pending, True=approved, False=rejected
    is_flagged: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    flagged_categories: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    flagged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    flagged_reason: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, default=None)

    # Duplicate detection: sha256 hash of normalized content
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)

    # Appeal system - creator can appeal flagged posts
    appeal_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    appeal_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    appeal_status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, default=None)  # pending/approved/denied
    appeal_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)
    appeal_decided_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    appeal_decided_by_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    tags_csv: Mapped[str] = mapped_column(String(255), nullable=False, default="")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Track when post was last edited (for report restrictions after appeal)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    saved_by: Mapped[list["SavedOpportunity"]] = relationship(
        back_populates="opportunity",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    creator_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ✅ FIXED - explicitly specify foreign key due to multiple FKs to User
    creator: Mapped["User"] = relationship("User", back_populates="posts", foreign_keys=[creator_user_id])



class SavedOpportunity(Base):
    __tablename__ = "saved_opportunities"
    __table_args__ = (
        UniqueConstraint("user_id", "opportunity_id", name="uq_user_opportunity"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship(back_populates="saved")
    opportunity: Mapped["Opportunity"] = relationship(back_populates="saved_by")

class RateLimit(Base):
    """
    DB-backed rate limiting. Tracks (user_id, action) with a sliding window.
    Window resets when now >= window_start + window_duration.
    """
    __tablename__ = "rate_limits"
    __table_args__ = (
        UniqueConstraint("user_id", "action", name="uq_user_action"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g. "create_opportunity", "update_opportunity"
    window_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("opportunity_id", "applicant_user_id", name="uq_application_once"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    applicant_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False, default="")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    decision_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default=None)

    decided_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    decided_by_user_id: Mapped[Optional[int]] = mapped_column(
    ForeignKey("users.id", ondelete="SET NULL"),
    nullable=True,
    index=True,
    )

    # relationships
    opportunity: Mapped["Opportunity"] = relationship()
    applicant: Mapped["User"] = relationship(foreign_keys=[applicant_user_id])
    decided_by: Mapped[Optional["User"]] = relationship(foreign_keys=[decided_by_user_id])


class ModerationLinkOpen(Base):
    """Log when a moderator opens or copies a user-submitted external URL (safe link review)."""
    __tablename__ = "moderation_link_opens"

    id: Mapped[int] = mapped_column(primary_key=True)

    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    moderator_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    action: Mapped[str] = mapped_column(String(20), nullable=False)  # OPEN, COPY
    normalized_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    host: Mapped[str] = mapped_column(String(253), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(10), nullable=False)  # LOW, MEDIUM, HIGH
    reasons: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array or comma-separated
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    opportunity: Mapped["Opportunity"] = relationship()
    moderator: Mapped["User"] = relationship(foreign_keys=[moderator_user_id])


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables ready.")


if __name__ == "__main__":
    asyncio.run(async_main())
