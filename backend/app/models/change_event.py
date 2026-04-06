import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ChangeEvent(Base):
    __tablename__ = "change_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tracked_account_id: Mapped[str] = mapped_column(String(36), ForeignKey("tracked_accounts.id"), nullable=False)
    previous_snapshot_id: Mapped[str] = mapped_column(String(36), ForeignKey("snapshots.id"), nullable=False)
    current_snapshot_id: Mapped[str] = mapped_column(String(36), ForeignKey("snapshots.id"), nullable=False)
    change_type: Mapped[str] = mapped_column(
        Enum("new_follower", "lost_follower", "new_following", "lost_following", name="change_type"),
        nullable=False,
    )
    instagram_username: Mapped[str] = mapped_column(String(255), nullable=False)
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tracked_account = relationship("TrackedAccount", back_populates="change_events")
    previous_snapshot = relationship("Snapshot", foreign_keys=[previous_snapshot_id])
    current_snapshot = relationship("Snapshot", foreign_keys=[current_snapshot_id])
