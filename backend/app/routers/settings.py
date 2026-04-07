from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/api/settings", tags=["settings"])


class SettingsResponse(BaseModel):
    notification_email_enabled: bool

    model_config = {"from_attributes": True}


class SettingsUpdate(BaseModel):
    notification_email_enabled: bool | None = None


@router.get("", response_model=SettingsResponse)
def get_settings(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("", response_model=SettingsResponse)
def update_settings(
    body: SettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if body.notification_email_enabled is not None:
        current_user.notification_email_enabled = body.notification_email_enabled
    db.commit()
    db.refresh(current_user)
    return current_user
