from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .fields import default
from .player import Player


@dataclass_json
@dataclass
class PlayerInfo:
    player: Player = default("playerInfo")
