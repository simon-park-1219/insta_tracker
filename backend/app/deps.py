from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.services.auth_service import decode_access_token
from app.services.scraper.base import BaseScraper
from app.services.scraper.mock_scraper import MockScraper
from app.services.scraper.instaloader_scraper import InstaLoaderScraper
from app.config import settings

security = HTTPBearer()

_scraper_instance: BaseScraper | None = None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    user_id = decode_access_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def get_scraper() -> BaseScraper:
    global _scraper_instance
    if _scraper_instance is None:
        if settings.scraper_mode == "instaloader":
            _scraper_instance = InstaLoaderScraper()
        else:
            _scraper_instance = MockScraper()
    return _scraper_instance
