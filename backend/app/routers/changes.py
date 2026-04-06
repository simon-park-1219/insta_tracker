from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import ChangeEvent, TrackedAccount, User
from app.schemas.change import ChangeEventResponse, ChangeSummary

router = APIRouter(prefix="/api", tags=["changes"])


@router.get("/accounts/{account_id}/changes", response_model=list[ChangeEventResponse])
def list_changes(
    account_id: str,
    change_type: str | None = None,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = (
        db.query(TrackedAccount)
        .filter(TrackedAccount.id == account_id, TrackedAccount.user_id == current_user.id)
        .first()
    )
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    query = db.query(ChangeEvent).filter(ChangeEvent.tracked_account_id == account_id)
    if change_type:
        query = query.filter(ChangeEvent.change_type == change_type)

    changes = query.order_by(ChangeEvent.detected_at.desc()).offset(offset).limit(limit).all()
    return changes


@router.get("/changes/summary", response_model=ChangeSummary)
def changes_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_accounts = (
        db.query(TrackedAccount.id)
        .filter(TrackedAccount.user_id == current_user.id)
        .subquery()
    )

    counts = (
        db.query(ChangeEvent.change_type, func.count(ChangeEvent.id))
        .filter(ChangeEvent.tracked_account_id.in_(db.query(user_accounts.c.id)))
        .group_by(ChangeEvent.change_type)
        .all()
    )

    summary = ChangeSummary()
    total = 0
    for change_type, count in counts:
        if change_type == "new_follower":
            summary.new_followers = count
        elif change_type == "lost_follower":
            summary.lost_followers = count
        elif change_type == "new_following":
            summary.new_following = count
        elif change_type == "lost_following":
            summary.lost_following = count
        total += count
    summary.total_changes = total
    return summary
