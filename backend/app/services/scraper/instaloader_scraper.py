import logging

from app.services.scraper.base import BaseScraper, ScraperResult

logger = logging.getLogger(__name__)


class InstaLoaderScraper(BaseScraper):
    """Real Instagram scraper using Instaloader.

    Requires a valid Instagram session cookie for accessing
    followers/following lists of non-public profiles.
    """

    def get_profile_data(self, username: str) -> ScraperResult:
        try:
            import instaloader

            loader = instaloader.Instaloader()
            profile = instaloader.Profile.from_username(loader.context, username)

            followers = [f.username for f in profile.get_followers()]
            following = [f.username for f in profile.get_followees()]

            return ScraperResult(
                followers=followers,
                following=following,
                follower_count=len(followers),
                following_count=len(following),
                success=True,
            )
        except Exception as e:
            logger.error(f"Instaloader scraping failed for {username}: {e}")
            return ScraperResult(
                followers=[],
                following=[],
                follower_count=0,
                following_count=0,
                success=False,
                error_message=str(e),
            )
