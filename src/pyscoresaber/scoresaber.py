import logging
from json.decoder import JSONDecodeError
from typing import List, Dict

import requests
from outcache import Cache

from .models import Player, Score
from .common import Common


class ScoreSaber:
    TIMEOUT = 10
    _url = "https://new.scoresaber.com/api"

    def __init__(self):
        self.log = logging.getLogger(__name__)

    def _process_url(self, url: str) -> Dict:
        response = Common.request(requests.get, url, timeout=self.TIMEOUT)

        try:
            data = response.json()
        except JSONDecodeError:
            self.log.exception("JSONDecodeError, response: %r, response.text: %r", response, response.text)
            data = {"error": "Failed to decode json from scoresaber. Somethings broken."}

        return data

    @Cache(minutes=2)
    def _get_player_basic(self, player_id: str) -> Dict:
        return self._process_url(f"{self._url}/player/{player_id}/basic")

    def get_player_basic(self, player_id: str) -> Player:
        response = self._get_player_basic(player_id)

        return Player.from_dict(response["playerInfo"])

    @Cache(minutes=2)
    def _get_player_full(self, player_id: str) -> Dict:
        return self._process_url(f"{self._url}/player/{player_id}/full")

    def get_player_full(self, player_id: str) -> Player:
        response = self._get_player_full(player_id)

        return Player.from_dict(response["playerInfo"])

    @Cache(minutes=2)
    def _get_recent_scores(self, player_id: str, page: int = 1) -> Dict:
        return self._process_url(f"{self._url}/player/{player_id}/scores/recent/{page}")

    def get_recent_scores(self, player_id: str, page: int = 1) -> List[Score]:
        response = self._get_recent_scores(player_id, page)

        recent_score_list = []

        for recent_score in response["scores"]:
            recent_score_list.append(Score.from_dict(recent_score))

        return recent_score_list

    @Cache(minutes=2)
    def _get_top_scores(self, player_id, page: int = 1) -> Dict:
        return self._process_url(f"{self._url}/player/{player_id}/scores/top/{page}")

    def get_top_scores(self, player_id, page: int = 1) -> List[Score]:
        response = self._get_top_scores(player_id, page)

        top_score_list = []

        for top_score in response["scores"]:
            top_score_list.append(Score.from_dict(top_score))

        return top_score_list
