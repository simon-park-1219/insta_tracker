import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Snapshot(Base):
    __tablename__ = "snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tracked_account_id: Mapped[str] = mapped_column(String(36), ForeignKey("tracked_accounts.id"), nullable=False)
    follower_count: Mapped[int] = mapped_column(Integer, default=0)
    following_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(Enum("success", "partial", "error", name="snapshot_status"), default="success")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    snapshot_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tracked_account = relationship("TrackedAccount", back_populates="snapshots")
    members = relationship("SnapshotMember", back_populates="snapshot", cascade="all, delete-orphan")


class SnapshotMember(Base):
    __tablename__ = "snapshot_members"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    snapshot_id: Mapped[str] = mapped_column(String(36), ForeignKey("snapshots.id"), nullable=False, index=True)
    instagram_username: Mapped[str] = mapped_column(String(255), nullable=False)
    relationship_type: Mapped[str] = mapped_column(
        Enum("follower", "following", name="relationship_type"), nullable=False
    )

    snapshot = relationship("Snapshot", back_populates="members")
