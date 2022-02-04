from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json

from .fields import datetime_field, default
from .leaderboard_player import LeaderBoardPlayer


@dataclass_json
@dataclass
class Score:
    """Score data from ScoreSaber"""

    id: int = default()
    leaderboard_player_info: Optional[LeaderBoardPlayer] = default("leaderboardPlayerInfo")
    rank: int = default()
    base_score: int = default("baseScore")
    modified_score: int = default("modifiedScore")
    pp: float = default()
    weight: float = default()
    modifiers: str = default()
    multiplier: int = default()
    bad_cuts: int = default("badCuts")
    missed_notes: int = default("missedNotes")
    max_combo: int = default("maxCombo")
    full_combo: bool = default("fullCombo")
    hmd: int = default()
    has_replay: bool = default("hasReplay")
    time_set: datetime = datetime_field("timeSet")
