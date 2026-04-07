import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.deps import get_scraper
from app.main import app
from app.services.scraper.mock_scraper import MockScraper

# Use file-based SQLite for tests (avoid threading issues)
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a fresh mock scraper for tests
_test_scraper = MockScraper()


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_scraper():
    return _test_scraper


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_scraper] = override_get_scraper


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    _test_scraper.reset()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture
def auth_token(client):
    r = client.post("/api/auth/register", json={"email": "test@test.com", "password": "test1234"})
    return r.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
