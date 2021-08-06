from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json

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
    country_rank: int = default("countryRank")
    pp: float = default()
    country: str = default()
    role: str = default()
    badges: List[str] = default()
    history: str = default()
    permissions: int = default()
    inactive: int = default()
    banned: int = default()

    score_stats: Optional[ScoreStats] = default("scoreStats")
