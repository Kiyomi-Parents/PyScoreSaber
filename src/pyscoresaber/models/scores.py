from dataclasses import dataclass
from typing import *

from dataclasses_json import dataclass_json

from .fields import default
from .score import Score


@dataclass_json
@dataclass
class Scores:
    scores: List[Score] = default()
