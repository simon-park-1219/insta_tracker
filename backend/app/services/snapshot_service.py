import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Snapshot, SnapshotMember, TrackedAccount
from app.services.scraper.base import BaseScraper

logger = logging.getLogger(__name__)


def take_snapshot(
    db: Session,
    account: TrackedAccount,
    scraper: BaseScraper,
    run_diff: bool = True,
) -> Snapshot:
    """Take a snapshot and optionally run diff + notifications."""
    result = scraper.get_profile_data(account.instagram_username)

    snapshot = Snapshot(
        tracked_account_id=account.id,
        follower_count=result.follower_count,
        following_count=result.following_count,
        status="success" if result.success else "error",
        error_message=result.error_message,
        snapshot_at=datetime.utcnow(),
    )
    db.add(snapshot)
    db.flush()

    if result.success:
        members = []
        for username in result.followers:
            members.append(
                SnapshotMember(
                    snapshot_id=snapshot.id,
                    instagram_username=username,
                    relationship_type="follower",
                )
            )
        for username in result.following:
            members.append(
                SnapshotMember(
                    snapshot_id=snapshot.id,
                    instagram_username=username,
                    relationship_type="following",
                )
            )
        db.add_all(members)

    account.last_checked_at = datetime.utcnow()
    db.commit()
    db.refresh(snapshot)

    # Run diff engine and create notifications
    if run_diff and result.success:
        try:
            from app.services.diff_engine import detect_changes
            from app.services.notification_service import create_notifications_for_changes
            from app.services.email_service import send_change_email

            changes = detect_changes(db, snapshot)
            if changes:
                create_notifications_for_changes(db, changes, account.user_id)
                # Send email notification
                user = account.user
                if user and user.notification_email_enabled:
                    send_change_email(user.email, account.instagram_username, changes)
                logger.info(
                    f"Detected {len(changes)} changes for @{account.instagram_username}"
                )
        except Exception as e:
            logger.error(f"Diff/notification failed for @{account.instagram_username}: {e}")

    return snapshot
