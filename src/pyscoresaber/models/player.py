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

    id: str
    name: str = default()
    profile_picture: str = default("profilePicture")
    country: str = default()
    pp: float = default()
    rank: int = default()
    country_rank: Optional[int] = default("countryRank")
    role: Optional[str] = default()
    badges: Optional[List[Badge]] = default()
    histories: str = default()
    score_stats: Optional[ScoreStats] = default("scoreStats")
    permissions: Optional[int] = default()
    banned: Optional[int] = default()
    inactive: Optional[int] = default()
