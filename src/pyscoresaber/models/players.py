from dataclasses import dataclass
from typing import *

from dataclasses_json import dataclass_json

from .fields import default
from .player import Player


@dataclass_json
@dataclass
class Players:
    players: List[Player] = default("players")
