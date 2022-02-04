from pprint import pprint
from typing import List

import pytest

from pyscoresaber import ScoreSaber, ScoreSaberAPI, ScoreSort

player_ids = [
    76561198029447509,
    76561198333869741,
    76561198187936410,
    76561198835772160,
    76561197995162898,
    76561198153101808,
    2538637699496776
]


# TODO: Add all the search filters
async def test_players(scoresaber: ScoreSaber):
    player_collection = await scoresaber.players()

    assert len(player_collection.players) > 0


async def test_players_count(scoresaber: ScoreSaber):
    players_count = await scoresaber.players_count()

    assert players_count > 0


@pytest.mark.parametrize("player_id", player_ids)
async def test_player_basic(scoresaber: ScoreSaber, player_id: int):
    player = await scoresaber.player_basic(player_id)

    assert int(player.id) == player_id


@pytest.mark.parametrize("player_ids", [player_ids])
async def test_players_basic(scoresaber: ScoreSaberAPI, player_ids: List[int]):
    async for player in scoresaber.players_basic(player_ids):
        assert int(player.id) in player_ids


@pytest.mark.parametrize("player_id", player_ids)
async def test_player_full(scoresaber: ScoreSaber, player_id: int):
    player = await scoresaber.player_full(player_id)

    assert int(player.id) == player_id


@pytest.mark.parametrize("player_ids", [player_ids])
async def test_players_full(scoresaber: ScoreSaberAPI, player_ids: List[int]):
    async for player in scoresaber.players_full(player_ids):
        assert int(player.id) in player_ids


@pytest.mark.parametrize("player_id", player_ids)
async def test_player_scores(scoresaber: ScoreSaber, player_id: int):
    player_score_collection = await scoresaber.player_scores(player_id)

    assert len(player_score_collection.player_scores) > 0

player_scores_all_test_data = [
    (76561198374231600, ScoreSort.TOP),
    (76561198374231600, ScoreSort.RECENT)
]


@pytest.mark.parametrize("player_id,score_sort", player_scores_all_test_data)
async def test_player_scores_all(scoresaber: ScoreSaberAPI, player_id: int, score_sort: ScoreSort):
    async for player_scores in scoresaber.player_scores_all(player_id, score_sort):
        assert len(player_scores) > 0
