from datetime import datetime

from pydantic import BaseModel


class ChangeEventResponse(BaseModel):
    id: str
    tracked_account_id: str
    change_type: str
    instagram_username: str
    detected_at: datetime

    model_config = {"from_attributes": True}


class ChangeSummary(BaseModel):
    new_followers: int = 0
    lost_followers: int = 0
    new_following: int = 0
    lost_following: int = 0
    total_changes: int = 0
