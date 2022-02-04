from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .fields import default
from .leaderboard_info import LeaderboardInfo
from .score import Score


@dataclass_json
@dataclass
class PlayerScore:
    """Player score data from ScoreSaber"""

    score: Score = default()
    leaderboard: LeaderboardInfo = default()
