from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from dataclasses_json import dataclass_json, LetterCase

from .difficulty import Difficulty
from .fields import default, datetime_field
from .score import Score


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LeaderboardInfo:
    """Leaderboard info data from ScoreSaber"""

    id: int
    song_hash: str
    song_name: str
    song_sub_name: str
    song_author_name: str
    level_author_name: str
    difficulty: Difficulty
    max_score: int
    ranked: bool
    qualified: bool
    loved: bool
    stars: int
    positive_modifiers: bool
    plays: int
    daily_plays: int
    cover_image: str
    player_score: Optional[Score]
    difficulties: Optional[List[Difficulty]]
    max_pp: int = default("maxPP")
    created_date: datetime = datetime_field("createdDate")
    ranked_date: Optional[datetime] = datetime_field("rankedDate")
    qualified_date: Optional[datetime] = datetime_field("qualifiedDate")
    loved_date: Optional[datetime] = datetime_field("lovedDate")
