import logging
from json.decoder import JSONDecodeError
import requests
from outcache import Cache

from .models import Player, Score
from .common import Common


class ScoreSaber:
    TIMEOUT = 10
    _url = "https://new.scoresaber.com/api"

    def __init__(self):
        self.log = logging.getLogger(__name__)

    def _process_url(self, url):
        response = Common.request(requests.get, url, timeout=self.TIMEOUT)

        try:
            data = response.json()
        except JSONDecodeError:
            self.log.exception("JSONDecodeError, response: %r, response.text: %r", response, response.text)
            data = {"error": "Failed to decode json from scoresaber. Somethings broken."}

        return data

    @Cache(minutes=2)
    def _get_player(self, player_id):
        return self._process_url(f"{self._url}/player/{player_id}/basic")

    def get_player(self, player_id):
        response = self._get_player(player_id)

        return Player(response["playerInfo"])

    @Cache(minutes=2)
    def _get_recent_scores(self, player_id):
        return self._process_url(f"{self._url}/player/{player_id}/scores/recent")

    def get_recent_scores(self, player_id):
        response = self._get_recent_scores(player_id)

        recent_score_list = []

        for recent_score in response["scores"]:
            recent_score_list.append(Score(recent_score))

        return recent_score_list

    @Cache(minutes=2)
    def _get_top_scores(self, player_id, page: int = 1):
        return self._process_url(f"{self._url}/player/{player_id}/scores/top/{page}")

    def get_top_scores(self, player_id, page: int = 1):
        response = self._get_top_scores(player_id, page)

        top_score_list = []

        for top_score in response["scores"]:
            top_score_list.append(Score(top_score))

        return top_score_list
