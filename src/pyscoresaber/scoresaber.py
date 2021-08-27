import asyncio
import logging
from asyncio import AbstractEventLoop
from typing import *

from faker import Faker
from outcache import CacheAsync

from .http_client import HttpClient
from .models import Player, Players, PlayerInfo, Score, Scores
from .scoresaber_provider import ScoreSaberProvider


class ScoreSaber:
    _url = "https://new.scoresaber.com/api"

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

    # /player

    @CacheAsync(hours=1)
    async def players(self,
        page: int = 1
    ) -> List[Player]:
        if self.test_mode:
            return self.faker.player_basic()

        players = await self._http_client.get(Players, f"{self._url}/players/{page}")
        return players.players

    @CacheAsync(minutes=2)
    async def player_basic(self,
        player_id: str
    ) -> Player:
        if self.test_mode:
            return self.faker.player_basic(player_id)

        player_info = await self._http_client.get(PlayerInfo, f"{self._url}/player/{player_id}/basic")
        return player_info.player

    @CacheAsync(minutes=2)
    async def player_full(self,
        player_id: str
    ) -> Player:
        if self.test_mode:
            return self.faker.player_full(player_id)

        player_info = await self._http_client.get(PlayerInfo, f"{self._url}/player/{player_id}/full")
        return player_info.player

    @CacheAsync(minutes=2)
    async def player_scores_recent(self,
        player_id: str,
        page: int = 1
    ) -> List[Score]:
        if self.test_mode:
            return self.faker.scores(8)

        scores = await self._http_client.get(Scores, f"{self._url}/player/{player_id}/scores/recent/{page}")
        return scores.scores

    @CacheAsync(minutes=2)
    async def player_scores_top(self,
        player_id: str,
        page: int = 1
    ) -> List[Score]:
        if self.test_mode:
            return self.faker.scores(8)

        scores = await self._http_client.get(Scores, f"{self._url}/player/{player_id}/scores/top/{page}")
        return scores.scores

