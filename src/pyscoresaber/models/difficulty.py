from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from .enum import BeatmapDifficulty, GameMode
from .fields import difficulty_field, game_mode_field


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Difficulty:
    """Difficulty data from ScoreSaber"""

    leaderboard_id: int
    difficulty_raw: str
    game_mode: GameMode = game_mode_field("gameMode")
    difficulty: BeatmapDifficulty = difficulty_field()
