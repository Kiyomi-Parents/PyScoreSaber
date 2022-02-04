from .base_enum import BaseEnum


class BeatmapDifficulty(BaseEnum):
    EASY = 1
    NORMAL = 3
    HARD = 5
    EXPERT = 7
    EXPERT_PLUS = 9
    UNKNOWN = -1
