from datetime import datetime

from pydantic import BaseModel


class AccountCreate(BaseModel):
    instagram_username: str
    display_name: str | None = None
    check_interval_minutes: int = 360


class AccountUpdate(BaseModel):
    display_name: str | None = None
    is_active: bool | None = None
    check_interval_minutes: int | None = None


class AccountResponse(BaseModel):
    id: str
    instagram_username: str
    display_name: str | None
    is_active: bool
    check_interval_minutes: int
    last_checked_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
