from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .fields import default


@dataclass_json
@dataclass
class ScoreStats:
    """Player score stats data from Score Saber"""

    total_score: int = default("totalScore")
    total_ranked_score: int = default("totalRankedScore")
    average_ranked_accuracy: float = default("averageRankedAccuracy")
    total_play_count: int = default("totalPlayCount")
    ranked_play_count: int = default("rankedPlayCount")
