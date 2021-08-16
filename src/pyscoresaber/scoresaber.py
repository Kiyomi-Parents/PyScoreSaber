import logging
from typing import List, Dict

from outcache import CacheAsync

from .httpClient import HttpClient
from .models import Player, Score


class ScoreSaber:
    TIMEOUT = 10
    _url = "https://new.scoresaber.com/api"

    def __init__(self):
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
        return await self._process_url('GET', f"{self._url}/player/{player_id}/basic")

    async def get_player_basic(self, player_id: str) -> Player:
        response = await self._get_player_basic(player_id)

        return Player.from_dict(response["playerInfo"])

    @CacheAsync(minutes=2)
    async def _get_player_full(self, player_id: str) -> Dict:
        return await self._process_url('GET', f"{self._url}/player/{player_id}/full")

    async def get_player_full(self, player_id: str) -> Player:
        response = await self._get_player_full(player_id)

        return Player.from_dict(response["playerInfo"])

    @CacheAsync(minutes=2)
    async def _get_recent_scores(self, player_id: str, page: int = 1) -> Dict:
        return await self._process_url('GET', f"{self._url}/player/{player_id}/scores/recent/{page}")

    async def get_recent_scores(self, player_id: str, page: int = 1) -> List[Score]:
        response = await self._get_recent_scores(player_id, page)

        recent_score_list = []

        for recent_score in response["scores"]:
            recent_score_list.append(Score.from_dict(recent_score))

        return recent_score_list

    @CacheAsync(minutes=2)
    async def _get_top_scores(self, player_id: str, page: int = 1) -> Dict:
        return await self._process_url('GET', f"{self._url}/player/{player_id}/scores/top/{page}")

    async def get_top_scores(self, player_id: str, page: int = 1) -> List[Score]:
        response = await self._get_top_scores(player_id, page)

        top_score_list = []

        for top_score in response["scores"]:
            top_score_list.append(Score.from_dict(top_score))

        return top_score_list
