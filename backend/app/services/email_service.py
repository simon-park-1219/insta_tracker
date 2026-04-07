import logging

from app.config import settings
from app.models import ChangeEvent

logger = logging.getLogger(__name__)


def send_change_email(email: str, account_username: str, changes: list[ChangeEvent]) -> None:
    """Send email notification about detected changes.

    In development mode, just logs to console instead of sending real emails.
    """
    if not changes:
        return

    subject = f"InstaTracker: {len(changes)} changes detected for @{account_username}"

    lines = [f"Changes detected for @{account_username}:\n"]
    for change in changes:
        prefix = {
            "new_follower": "+follower",
            "lost_follower": "-follower",
            "new_following": "+following",
            "lost_following": "-following",
        }.get(change.change_type, change.change_type)
        lines.append(f"  [{prefix}] {change.instagram_username}")

    body = "\n".join(lines)

    if settings.app_env == "development":
        logger.info(f"[DEV EMAIL] To: {email}\nSubject: {subject}\n{body}")
        return

    # Production email sending via SMTP
    try:
        import asyncio
        from email.message import EmailMessage
        import aiosmtplib

        msg = EmailMessage()
        msg["From"] = settings.email_from
        msg["To"] = email
        msg["Subject"] = subject
        msg.set_content(body)

        asyncio.get_event_loop().run_until_complete(
            aiosmtplib.send(
                msg,
                hostname=settings.smtp_host,
                port=settings.smtp_port,
                username=settings.smtp_user or None,
                password=settings.smtp_password or None,
            )
        )
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
