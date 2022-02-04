from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json, LetterCase

from .metadata import Metadata
from .player import Player


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PlayerCollection:
    """Player collection data from ScoreSaber"""

    players: List[Player]
    metadata: Metadata
