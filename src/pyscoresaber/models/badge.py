from dataclasses import dataclass

from dataclasses_json import dataclass_json

from pyscoresaber.models.fields import default


@dataclass_json
@dataclass
class Badge:
    image: str = default()
    description: str = default()
