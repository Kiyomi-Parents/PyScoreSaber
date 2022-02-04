import math
from typing import *

from .scoresaber import ScoreSaber
from .models import *


class ScoreSaberAPI(ScoreSaber):
    async def players_basic(self, player_ids: List[int]) -> AsyncIterable[Player]:
        for player_id in player_ids:
            yield await self.player_basic(player_id)

    async def players_full(self, player_ids: List[int]) -> AsyncIterable[Player]:
        for player_id in player_ids:
            yield await self.player_full(player_id)

    async def player_scores_all(self, player_id: int, score_sort: ScoreSort) -> AsyncIterable[List[Score]]:
        page = 0
        max_page = -1

        while page < max_page or max_page == -1:
            recent_scores = await self.player_scores(player_id, sort=score_sort, limit=100, page=page)

            if max_page == -1:
                max_page = math.ceil(recent_scores.metadata.total / 100) + 1

            yield recent_scores.player_scores

            page += 1
