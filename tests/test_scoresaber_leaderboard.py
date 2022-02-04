import json

import pytest

from src.pyscoresaber import ScoreSaber, BeatmapDifficulty, GameMode
from src.pyscoresaber.models.fields import game_mode_decoder, difficulty_decoder


def get_static_leaderboards():
    with open("tests/data/leaderboards.json", "r") as file:
        return json.load(file)


# TODO: Add all the search filters
async def test_leaderboards(scoresaber: ScoreSaber):
    leaderboards = await scoresaber.leaderboards()

    assert len(leaderboards.leaderboards) > 0


def leaderboard_info_by_id_test_data():
    data = []
    leaderboards = get_static_leaderboards()

    for leaderboard in leaderboards:
        data.append(leaderboard["id"])

    return data


@pytest.mark.parametrize("leaderboard_id", leaderboard_info_by_id_test_data())
async def test_leaderboard_by_id(scoresaber: ScoreSaber, leaderboard_id: int):
    leaderboard_info = await scoresaber.leaderboard_info_by_id(leaderboard_id)

    assert leaderboard_info.id == leaderboard_id


def leaderboard_info_by_hash_test_data():
    data = []
    leaderboards = get_static_leaderboards()

    for leaderboard in leaderboards:
        for difficulty in leaderboard["difficulties"]:
            data.append(
                (
                    leaderboard["songHash"],
                    difficulty_decoder(difficulty["difficulty"]),
                    game_mode_decoder(difficulty["gameMode"])
                )
            )

    return data


@pytest.mark.parametrize("leaderboard_hash,beatmap_difficulty,beatmap_game_mode", leaderboard_info_by_hash_test_data())
async def test_leaderboard_info_by_hash(scoresaber: ScoreSaber, leaderboard_hash: str, beatmap_difficulty: BeatmapDifficulty, beatmap_game_mode: GameMode):
    leaderboard_info = await scoresaber.leaderboard_info_by_hash(leaderboard_hash, beatmap_difficulty, beatmap_game_mode)

    assert leaderboard_info.song_hash in leaderboard_hash
    assert leaderboard_info.difficulty.difficulty == beatmap_difficulty
    assert leaderboard_info.difficulty.game_mode == beatmap_game_mode


@pytest.mark.parametrize("leaderboard_id", leaderboard_info_by_id_test_data())
async def test_leaderboard_scores_by_id(scoresaber: ScoreSaber, leaderboard_id: int):
    score_collection = await scoresaber.leaderboard_scores_by_id(leaderboard_id)

    assert len(score_collection.scores) > 0


@pytest.mark.parametrize("leaderboard_hash,beatmap_difficulty,beatmap_game_mode", leaderboard_info_by_hash_test_data())
async def test_leaderboard_scores_by_hash(scoresaber: ScoreSaber, leaderboard_hash, beatmap_difficulty, beatmap_game_mode):
    score_collection = await scoresaber.leaderboard_scores_by_hash(leaderboard_hash, beatmap_difficulty, game_mode=beatmap_game_mode)

    assert len(score_collection.scores) > 0


def leaderboard_difficulties_test_data():
    data = []
    leaderboards = get_static_leaderboards()

    for leaderboard in leaderboards:
        data.append(leaderboard["songHash"])

    return data


@pytest.mark.parametrize("leaderboard_hash", leaderboard_difficulties_test_data())
async def test_leaderboard_difficulties(scoresaber: ScoreSaber, leaderboard_hash: str):
    difficulties = await scoresaber.leaderboard_difficulties(leaderboard_hash)

    assert len(difficulties) > 0
