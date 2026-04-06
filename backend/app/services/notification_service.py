from sqlalchemy.orm import Session

from app.models import ChangeEvent, Notification, TrackedAccount

_CHANGE_TYPE_LABELS = {
    "new_follower": ("New Follower", "{username} started following @{account}"),
    "lost_follower": ("Lost Follower", "{username} unfollowed @{account}"),
    "new_following": ("New Following", "@{account} started following {username}"),
    "lost_following": ("Unfollowed", "@{account} unfollowed {username}"),
}


def create_notifications_for_changes(
    db: Session, changes: list[ChangeEvent], user_id: str,
) -> list[Notification]:
    """Create in-app notifications for detected changes."""
    if not changes:
        return []

    # Get account username for message formatting
    account = db.query(TrackedAccount).filter(
        TrackedAccount.id == changes[0].tracked_account_id
    ).first()
    account_name = account.instagram_username if account else "unknown"

    notifications = []
    for change in changes:
        title, message_template = _CHANGE_TYPE_LABELS.get(
            change.change_type, ("Change Detected", "{username} - @{account}")
        )
        message = message_template.format(
            username=change.instagram_username, account=account_name
        )
        notification = Notification(
            user_id=user_id,
            change_event_id=change.id,
            title=title,
            message=message,
        )
        notifications.append(notification)

    db.add_all(notifications)
    db.commit()
    return notifications
