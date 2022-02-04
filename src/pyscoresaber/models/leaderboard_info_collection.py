from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from .fields import default
from .leaderboard_info import LeaderboardInfo
from .metadata import Metadata


@dataclass_json
@dataclass
class LeaderboardInfoCollection:
    """Leaderboard info collection data from ScoreSaber"""

    leaderboards: List[LeaderboardInfo] = default()
    metadata: Metadata = default()
