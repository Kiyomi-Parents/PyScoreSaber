import asyncio
import logging
from asyncio import AbstractEventLoop
from typing import *

from faker import Faker
from outcache import CacheAsync

from .http_client import HttpClient
from .models import *
from .scoresaber_provider import ScoreSaberProvider


class ScoreSaber:
    _url = "https://scoresaber.com/api"

    def __init__(self, loop: Optional[AbstractEventLoop] = None, test_mode: bool = False):
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.test_mode = test_mode

        self.log = logging.getLogger(__name__)
        self._http_client = HttpClient(self.loop)

        if test_mode:
            self.faker = Faker()
            Faker.seed(76561198283584459)
            self.faker.add_provider(ScoreSaberProvider)

    async def start(self):
        await self._http_client.start()

    async def close(self):
        await self._http_client.close()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    # /leaderboard

    @CacheAsync(hours=1)
    async def leaderboards(self,
        search: Optional[str] = None,
        ranked: Optional[bool] = None,
        qualified: Optional[bool] = None,
        loved: Optional[bool] = None,
        min_star: Optional[int] = None,
        max_star: Optional[int] = None,
        category: Optional[Category] = None,
        sort: Optional[Sort] = None,
        unique: Optional[bool] = None,
        page: Optional[int] = None
    ) -> LeaderboardInfoCollection:
        if self.test_mode:
            raise RuntimeError("Not implemented!")

        url = f"{self._url}/leaderboards"
        params = {
            "search": search, "ranked": ranked, "qualified": qualified,
            "loved": loved, "minStar": min_star, "maxStar": max_star,
            "category": category, "sort": sort, "unique": unique, "page": page
        }

        return await self._http_client.get(LeaderboardInfoCollection, url, params)

    @CacheAsync(hours=1)
    async def leaderboard_info_by_id(self,
        leaderboard_id: int
    ) -> LeaderboardInfo:
        if self.test_mode:
            raise RuntimeError("Not implemented!")

        return await self._http_client.get(LeaderboardInfo, f"{self._url}/leaderboard/by-id/{leaderboard_id}/info")

    @CacheAsync(hours=1)
    async def leaderboard_info_by_hash(self,
        beatmap_hash: str,
        difficulty: BeatmapDifficulty,
        game_mode: Optional[GameMode] = None
    ) -> LeaderboardInfo:
        if self.test_mode:
            raise RuntimeError("Not implemented!")

        url = f"{self._url}/leaderboard/by-hash/{beatmap_hash}/info"
        params = {
            "difficulty": difficulty, "gameMode": game_mode
        }

        return await self._http_client.get(LeaderboardInfo, url, params)

    @CacheAsync(hours=1)
    async def leaderboard_scores_by_id(self,
        leaderboard_id: int,
        countries: Optional[str] = None,
        search: Optional[str] = None,
        page: Optional[int] = None
    ) -> ScoreCollection:
        if self.test_mode:
            raise RuntimeError("Not implemented!")

        url = f"{self._url}/leaderboard/by-id/{leaderboard_id}/scores"
        params = {
            "countries": countries, "search": search, "page": page
        }

        return await self._http_client.get(ScoreCollection, url, params)

    @CacheAsync(hours=1)
    async def leaderboard_scores_by_hash(self,
        beatmap_hash: str,
        difficulty: BeatmapDifficulty,
        countries: Optional[str] = None,
        search: Optional[str] = None,
        page: Optional[int] = None,
        game_mode: Optional[GameMode] = None
    ) -> ScoreCollection:
        if self.test_mode:
            raise RuntimeError("Not implemented!")

        url = f"{self._url}/leaderboard/by-hash/{beatmap_hash}/scores"
        params = {
            "difficulty": difficulty, "countries": countries, "search": search,
            "page": page, "gameMode": game_mode
        }

        return await self._http_client.get(ScoreCollection, url, params)

    @CacheAsync(hours=1)
    async def leaderboard_difficulties(self,
        beatmap_hash: str
    ) -> List[Difficulty]:
        if self.test_mode:
            raise RuntimeError("Not implemented!")

        return await self._http_client.get(List[Difficulty], f"{self._url}/leaderboard/get-difficulties/{beatmap_hash}")

    # /player

    @CacheAsync(minutes=10)
    async def players(self,
        search: Optional[str] = None,
        page: Optional[int] = None,
        countries: Optional[str] = None
    ) -> PlayerCollection:
        if self.test_mode:
            raise RuntimeError("Not implemented!")

        url = f"{self._url}/players"
        params = {
            "search": search, "page": page, "countries": countries
        }

        return await self._http_client.get(PlayerCollection, url, params)

    @CacheAsync(hours=1)
    async def players_count(self,
        search: Optional[str] = None,
        countries: Optional[str] = None
    ) -> int:
        if self.test_mode:
            raise RuntimeError("Not implemented!")

        url = f"{self._url}/players/count"
        params = {
            "search": search, "countries": countries
        }

        return await self._http_client.get(int, url, params)

    @CacheAsync(minutes=1)
    async def player_basic(self,
        player_id: int
    ) -> Player:
        if self.test_mode:
            raise RuntimeError("Not implemented!")

        return await self._http_client.get(Player, f"{self._url}/player/{player_id}/basic")

    @CacheAsync(minutes=1)
    async def player_full(self,
        player_id: int
    ) -> Player:
        if self.test_mode:
            raise RuntimeError("Not implemented!")

        return await self._http_client.get(Player, f"{self._url}/player/{player_id}/full")

    @CacheAsync(minutes=1)
    async def player_scores(self,
        player_id: int,
        limit: Optional[int] = None,
        sort: Optional[ScoreSort] = None,
        page: Optional[int] = None
    ) -> PlayerScoresCollection:
        if self.test_mode:
            raise RuntimeError("Not implemented!")

        url = f"{self._url}/player/{player_id}/scores"
        params = {
            "limit": limit, "sort": sort, "page": page
        }

        return await self._http_client.get(PlayerScoresCollection, url, params)

    # /user

    # TODO: Implement GET /user/{player_id}/refresh
    # TODO: Implement GET /user/@me
    # TODO: Implement GET /user/quest-key

    # /ranking

    # TODO: Implement GET /ranking/requests/top
    # TODO: Implement GET /ranking/requests/belowTop
    # TODO: Implement GET /ranking/request/{request_id}
    # TODO: Implement GET /ranking/request/by-id/{leaderboard_id}

    # TODO: Implement POST /ranking/request/action/rt/create
    # TODO: Implement POST /ranking/request/action/rt/vote
    # TODO: Implement POST /ranking/request/action/rt/comment

    # TODO: Implement POST /ranking/request/action/qat/vote
    # TODO: Implement POST /ranking/request/action/qat/comment

    # TODO: Implement POST /ranking/request/action/nat/replace
    # TODO: Implement POST /ranking/request/action/nat/qualify
    # TODO: Implement POST /ranking/request/action/nat/deny
