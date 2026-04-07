from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, get_scraper
from app.models import TrackedAccount, User
from app.schemas.account import AccountCreate, AccountResponse, AccountUpdate
from app.services.scraper.base import BaseScraper
from app.services.snapshot_service import take_snapshot

router = APIRouter(prefix="/api/accounts", tags=["accounts"])


@router.get("", response_model=list[AccountResponse])
def list_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    accounts = (
        db.query(TrackedAccount)
        .filter(TrackedAccount.user_id == current_user.id)
        .order_by(TrackedAccount.created_at.desc())
        .all()
    )
    return accounts


@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    body: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = TrackedAccount(
        user_id=current_user.id,
        instagram_username=body.instagram_username,
        display_name=body.display_name,
        check_interval_minutes=body.check_interval_minutes,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = _get_user_account(db, current_user.id, account_id)
    return account


@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: str,
    body: AccountUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = _get_user_account(db, current_user.id, account_id)
    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = _get_user_account(db, current_user.id, account_id)
    db.delete(account)
    db.commit()


@router.post("/{account_id}/snapshots")
def trigger_snapshot(
    account_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    scraper: BaseScraper = Depends(get_scraper),
):
    account = _get_user_account(db, current_user.id, account_id)
    snapshot = take_snapshot(db, account, scraper)
    return {
        "id": snapshot.id,
        "follower_count": snapshot.follower_count,
        "following_count": snapshot.following_count,
        "status": snapshot.status,
        "snapshot_at": str(snapshot.snapshot_at),
    }


@router.get("/{account_id}/snapshots")
def list_snapshots(
    account_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
):
    account = _get_user_account(db, current_user.id, account_id)
    from app.models import Snapshot

    snapshots = (
        db.query(Snapshot)
        .filter(Snapshot.tracked_account_id == account.id)
        .order_by(Snapshot.snapshot_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return snapshots


def _get_user_account(db: Session, user_id: str, account_id: str) -> TrackedAccount:
    account = (
        db.query(TrackedAccount)
        .filter(TrackedAccount.id == account_id, TrackedAccount.user_id == user_id)
        .first()
    )
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
