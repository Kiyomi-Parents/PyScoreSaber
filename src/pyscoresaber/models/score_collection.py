from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json, LetterCase

from .metadata import Metadata
from .score import Score


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ScoreCollection:
    scores: List[Score]
    metadata: Metadata
