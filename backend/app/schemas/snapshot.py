from datetime import datetime

from pydantic import BaseModel


class SnapshotResponse(BaseModel):
    id: str
    tracked_account_id: str
    follower_count: int
    following_count: int
    status: str
    error_message: str | None
    snapshot_at: datetime

    model_config = {"from_attributes": True}


class SnapshotMemberResponse(BaseModel):
    instagram_username: str
    relationship_type: str

    model_config = {"from_attributes": True}


class SnapshotDetailResponse(SnapshotResponse):
    members: list[SnapshotMemberResponse] = []
