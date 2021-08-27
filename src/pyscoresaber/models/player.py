from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json

from .badge import Badge
from .fields import default
from .score_stats import ScoreStats


@dataclass_json
@dataclass
class Player:
    """Player data from ScoreSaber"""

    player_id: str = default("playerId")
    player_name: str = default("playerName")
    avatar: str = default()
    rank: int = default()
    country_rank: Optional[int] = default("countryRank")
    pp: float = default()
    country: str = default()
    role: Optional[str] = default()
    badges: Optional[List[Badge]] = default()
    history: str = default()
    permissions: Optional[int] = default()
    inactive: Optional[int] = default()
    banned: Optional[int] = default()
    difference: Optional[int] = default()

    score_stats: Optional[ScoreStats] = default("scoreStats")
