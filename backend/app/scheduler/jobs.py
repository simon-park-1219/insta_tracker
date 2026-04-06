import logging

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.deps import get_scraper
from app.models import TrackedAccount
from app.services.snapshot_service import take_snapshot

logger = logging.getLogger(__name__)


def run_scheduled_snapshots():
    """Check all active tracked accounts and take snapshots when due."""
    db: Session = SessionLocal()
    try:
        scraper = get_scraper()
        accounts = db.query(TrackedAccount).filter(TrackedAccount.is_active.is_(True)).all()

        for account in accounts:
            if _is_due(account):
                logger.info(f"Taking scheduled snapshot for @{account.instagram_username}")
                try:
                    take_snapshot(db, account, scraper)
                except Exception as e:
                    logger.error(f"Snapshot failed for @{account.instagram_username}: {e}")
    finally:
        db.close()


def _is_due(account: TrackedAccount) -> bool:
    if account.last_checked_at is None:
        return True

    from datetime import datetime, timedelta

    next_check = account.last_checked_at + timedelta(minutes=account.check_interval_minutes)
    return datetime.utcnow() >= next_check
