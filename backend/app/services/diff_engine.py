from datetime import datetime

from sqlalchemy.orm import Session

from app.models import ChangeEvent, Snapshot, SnapshotMember


def detect_changes(db: Session, current_snapshot: Snapshot) -> list[ChangeEvent]:
    """Compare current snapshot with the previous one and return change events."""
    previous_snapshot = (
        db.query(Snapshot)
        .filter(
            Snapshot.tracked_account_id == current_snapshot.tracked_account_id,
            Snapshot.id != current_snapshot.id,
            Snapshot.status == "success",
        )
        .order_by(Snapshot.snapshot_at.desc())
        .first()
    )

    if not previous_snapshot:
        return []

    prev_followers = _get_members(db, previous_snapshot.id, "follower")
    curr_followers = _get_members(db, current_snapshot.id, "follower")
    prev_following = _get_members(db, previous_snapshot.id, "following")
    curr_following = _get_members(db, current_snapshot.id, "following")

    changes: list[ChangeEvent] = []
    now = datetime.utcnow()

    # New followers
    for username in curr_followers - prev_followers:
        changes.append(_make_event(
            current_snapshot, previous_snapshot, "new_follower", username, now
        ))

    # Lost followers
    for username in prev_followers - curr_followers:
        changes.append(_make_event(
            current_snapshot, previous_snapshot, "lost_follower", username, now
        ))

    # New following
    for username in curr_following - prev_following:
        changes.append(_make_event(
            current_snapshot, previous_snapshot, "new_following", username, now
        ))

    # Lost following
    for username in prev_following - curr_following:
        changes.append(_make_event(
            current_snapshot, previous_snapshot, "lost_following", username, now
        ))

    if changes:
        db.add_all(changes)
        db.commit()

    return changes


def _get_members(db: Session, snapshot_id: str, relationship_type: str) -> set[str]:
    rows = (
        db.query(SnapshotMember.instagram_username)
        .filter(
            SnapshotMember.snapshot_id == snapshot_id,
            SnapshotMember.relationship_type == relationship_type,
        )
        .all()
    )
    return {r[0] for r in rows}


def _make_event(
    current: Snapshot, previous: Snapshot,
    change_type: str, username: str, now: datetime,
) -> ChangeEvent:
    return ChangeEvent(
        tracked_account_id=current.tracked_account_id,
        previous_snapshot_id=previous.id,
        current_snapshot_id=current.id,
        change_type=change_type,
        instagram_username=username,
        detected_at=now,
    )
