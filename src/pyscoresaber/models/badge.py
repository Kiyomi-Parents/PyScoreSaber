from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .fields import default


@dataclass_json
@dataclass
class Badge:
    """Badge info from Score Saber"""
    description: str = default()
    image: str = default()
