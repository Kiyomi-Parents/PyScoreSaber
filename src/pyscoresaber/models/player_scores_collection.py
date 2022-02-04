from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json, LetterCase

from .metadata import Metadata
from .player_score import PlayerScore


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PlayerScoresCollection:
    """Player scores collection data from ScoreSaber"""

    player_scores: List[PlayerScore]
    metadata: Metadata
