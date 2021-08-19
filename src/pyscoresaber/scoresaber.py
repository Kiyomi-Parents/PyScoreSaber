import logging
from typing import List, Dict

from faker import Faker
from outcache import CacheAsync

from .http_client import HttpClient
from .models import Player, Score
from .scoresaber_provider import ScoreSaberProvider


class ScoreSaber:
    TIMEOUT = 10
    _url = "https://new.scoresaber.com/api"

    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode

        if test_mode:
            self.faker = Faker()
            Faker.seed(76561198283584459)
            self.faker.add_provider(ScoreSaberProvider)

        self.log = logging.getLogger(__name__)
        self._http = HttpClient()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def start(self):
        await self._http.start()

    async def close(self):
        await self._http.close()

    async def _process_url(self, method: str, url: str) -> Dict:
        await self._http.start()

        return await self._http.request(method, url, timeout=self.TIMEOUT)

    @CacheAsync(minutes=2)
    async def _get_player_basic(self, player_id: str) -> Dict:
        if self.test_mode:
            return {"playerInfo": self.faker.player_basic().to_dict()}

        return await self._process_url('GET', f"{self._url}/player/{player_id}/basic")

    async def get_player_basic(self, player_id: str) -> Player:
        response = await self._get_player_basic(player_id)

        return Player.from_dict(response["playerInfo"])

    @CacheAsync(minutes=2)
    async def _get_player_full(self, player_id: str) -> Dict:
        if self.test_mode:
            return {"playerInfo": self.faker.player_full().to_dict()}

        return await self._process_url('GET', f"{self._url}/player/{player_id}/full")

    async def get_player_full(self, player_id: str) -> Player:
        response = await self._get_player_full(player_id)

        return Player.from_dict(response["playerInfo"])

    @CacheAsync(minutes=2)
    async def _get_recent_scores(self, player_id: str, page: int = 1) -> Dict:
        if self.test_mode:
            return {"scores": [score.to_dict() for score in self.faker.scores(8)]}

        return await self._process_url('GET', f"{self._url}/player/{player_id}/scores/recent/{page}")

    async def get_recent_scores(self, player_id: str, page: int = 1) -> List[Score]:
        response = await self._get_recent_scores(player_id, page)

        recent_score_list = []

        for recent_score in response["scores"]:
            recent_score_list.append(Score.from_dict(recent_score))

        return recent_score_list

    @CacheAsync(minutes=2)
    async def _get_top_scores(self, player_id: str, page: int = 1) -> Dict:
        if self.test_mode:
            return {"scores": [score.to_dict() for score in self.faker.scores(8)]}

        return await self._process_url('GET', f"{self._url}/player/{player_id}/scores/top/{page}")

    async def get_top_scores(self, player_id: str, page: int = 1) -> List[Score]:
        response = await self._get_top_scores(player_id, page)

        top_score_list = []

        for top_score in response["scores"]:
            top_score_list.append(Score.from_dict(top_score))

        return top_score_list
