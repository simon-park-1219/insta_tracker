from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import TrackedAccount, Snapshot, SnapshotMember, User
from app.services.diff_engine import detect_changes
from app.services.auth_service import hash_password


def _setup():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_detect_new_and_lost_followers():
    db = _setup()

    user = User(email="u@test.com", password_hash=hash_password("p"))
    db.add(user)
    db.flush()

    acct = TrackedAccount(user_id=user.id, instagram_username="target")
    db.add(acct)
    db.flush()

    # Snapshot 1: followers = [a, b, c]
    snap1 = Snapshot(tracked_account_id=acct.id, follower_count=3, following_count=0)
    db.add(snap1)
    db.flush()
    for name in ["a", "b", "c"]:
        db.add(SnapshotMember(snapshot_id=snap1.id, instagram_username=name, relationship_type="follower"))
    db.commit()

    # Snapshot 2: followers = [b, c, d] (lost a, gained d)
    snap2 = Snapshot(tracked_account_id=acct.id, follower_count=3, following_count=0)
    db.add(snap2)
    db.flush()
    for name in ["b", "c", "d"]:
        db.add(SnapshotMember(snapshot_id=snap2.id, instagram_username=name, relationship_type="follower"))
    db.commit()

    changes = detect_changes(db, snap2)

    types = {(c.change_type, c.instagram_username) for c in changes}
    assert ("new_follower", "d") in types
    assert ("lost_follower", "a") in types
    assert len(changes) == 2


def test_no_changes_on_first_snapshot():
    db = _setup()

    user = User(email="u2@test.com", password_hash=hash_password("p"))
    db.add(user)
    db.flush()

    acct = TrackedAccount(user_id=user.id, instagram_username="target2")
    db.add(acct)
    db.flush()

    snap1 = Snapshot(tracked_account_id=acct.id, follower_count=2, following_count=0)
    db.add(snap1)
    db.flush()
    for name in ["x", "y"]:
        db.add(SnapshotMember(snapshot_id=snap1.id, instagram_username=name, relationship_type="follower"))
    db.commit()

    changes = detect_changes(db, snap1)
    assert len(changes) == 0
