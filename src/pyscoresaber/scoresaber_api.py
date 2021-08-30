from typing import *

from . import ScoreSaber
from .models import *


class ScoreSaberAPI(ScoreSaber):
    async def players_basic(self, player_ids: List[str]) -> AsyncIterable[Player]:
        for player_id in player_ids:
            yield await self.player_basic(player_id)

    async def players_full(self, player_ids: List[str]) -> AsyncIterable[Player]:
        for player_id in player_ids:
            yield await self.player_full(player_id)

    async def player_scores_recent_all(self, player_id: str) -> AsyncIterable[List[Score]]:
        page = 0
        while True:
            recent_scores = await self.player_scores_recent(player_id, page)

            if len(recent_scores) == 0:
                break

            yield recent_scores

            page += 1

    async def player_scores_top_all(self, player_id: str) -> AsyncIterable[List[Score]]:
        page = 0

        while True:
            top_scores = await self.player_scores_top(player_id, page)

            if len(top_scores) == 0:
                break

            yield top_scores

            page += 1
