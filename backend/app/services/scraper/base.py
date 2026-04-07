from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ScraperResult:
    followers: list[str]
    following: list[str]
    follower_count: int
    following_count: int
    success: bool
    error_message: str | None = None


class BaseScraper(ABC):
    @abstractmethod
    def get_profile_data(self, username: str) -> ScraperResult:
        """Fetch followers and following for a given Instagram username."""
        ...
