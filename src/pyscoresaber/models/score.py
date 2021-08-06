from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json

from pyscoresaber.models.fields import datetime_field, default


@dataclass_json
@dataclass
class Score:
    """Score data from ScoreSaber"""

    rank: int = default()
    score_id: int = default("scoreId")
    score: int = default()
    unmodified_score: int = default("unmodififiedScore")
    mods: str = default()
    pp: float = default()
    weight: float = default()
    time_set: datetime = datetime_field("timeSet")
    leaderboard_id: int = default("leaderboardId")
    song_hash: str = default("songHash")
    song_name: str = default("songName")
    song_sub_name: str = default("songSubName")
    song_author_name: str = default("songAuthorName")
    level_author_name: str = default("levelAuthorName")
    difficulty: int = default()
    difficulty_raw: str = default("difficultyRaw")
    max_score: int = default("maxScore")
