from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json

from .fields import default


@dataclass_json
@dataclass
class LeaderBoardPlayer:
    """Leaderboard player data from ScoreSaber"""

    id: str = default()
    name: str = default()
    profile_picture: str = default("profilePicture")
    country: str = default()
    permissions: int = default()
    role: Optional[str] = default()
