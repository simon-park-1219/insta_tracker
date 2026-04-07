import hashlib
import random

from app.services.scraper.base import BaseScraper, ScraperResult

# Pool of fake usernames for generating mock data
_FAKE_USERS = [
    "alex_photo", "bella_design", "charlie_dev", "diana_art", "evan_music",
    "fiona_travel", "george_fit", "hannah_cook", "ivan_tech", "julia_style",
    "kevin_game", "luna_yoga", "marco_film", "nina_books", "oscar_skate",
    "petra_dance", "quinn_surf", "rosa_paint", "sam_hike", "tina_sing",
    "uma_write", "victor_code", "wendy_run", "xander_climb", "yuki_craft",
    "zara_food", "amber_blog", "blake_dj", "cora_model", "derek_photo2",
    "ella_swim", "frank_build", "grace_plant", "hugo_ride", "iris_draw",
    "jake_fly", "kate_read", "leo_camp", "maya_knit", "nate_brew",
    "olive_fish", "paul_sail", "rue_garden", "steve_gym", "tara_bake",
    "uri_explore", "val_create", "wade_snap", "xena_move", "yara_dream",
]


class MockScraper(BaseScraper):
    """Mock scraper that generates deterministic but evolving fake data.

    Uses the username as a seed, and introduces small random changes
    each time to simulate real follower/following churn.
    """

    _state: dict[str, dict[str, set[str]]] = {}

    def get_profile_data(self, username: str) -> ScraperResult:
        if username not in self._state:
            self._initialize(username)
        else:
            self._evolve(username)

        followers = sorted(self._state[username]["followers"])
        following = sorted(self._state[username]["following"])

        return ScraperResult(
            followers=followers,
            following=following,
            follower_count=len(followers),
            following_count=len(following),
            success=True,
        )

    def _initialize(self, username: str) -> None:
        seed = int(hashlib.md5(username.encode()).hexdigest(), 16) % (2**32)
        rng = random.Random(seed)

        follower_count = rng.randint(15, 35)
        following_count = rng.randint(10, 30)

        pool = list(_FAKE_USERS)
        rng.shuffle(pool)

        followers = set(pool[:follower_count])
        remaining = [u for u in pool if u not in followers]
        following = set(remaining[:following_count])

        self._state[username] = {"followers": followers, "following": following}

    def _evolve(self, username: str) -> None:
        """Simulate small changes: 1-3 followers/following gained or lost."""
        state = self._state[username]

        for rel_type in ["followers", "following"]:
            current = state[rel_type]
            all_possible = set(_FAKE_USERS)
            not_in = all_possible - current

            # Lose 0-2
            lose_count = random.randint(0, min(2, len(current)))
            if lose_count > 0:
                to_lose = random.sample(sorted(current), lose_count)
                current -= set(to_lose)

            # Gain 0-2
            gain_count = random.randint(0, min(2, len(not_in)))
            if gain_count > 0:
                to_gain = random.sample(sorted(not_in), gain_count)
                current |= set(to_gain)
