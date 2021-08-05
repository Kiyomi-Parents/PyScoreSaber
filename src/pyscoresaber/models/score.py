from dateutil import parser, tz


class Score:
    """Score data from ScoreSaber"""

    def __init__(self, score_json):
        self.rank = score_json["rank"]
        self.scoreId = score_json["scoreId"]
        self.score = score_json["score"]
        self.unmodififiedScore = score_json["unmodififiedScore"]
        self.mods = score_json["mods"]
        self.pp = score_json["pp"]
        self.weight = score_json["weight"]
        self.timeSet = parser.isoparse(score_json["timeSet"]).replace(tzinfo=None)
        self.leaderboardId = score_json["leaderboardId"]
        self.songHash = score_json["songHash"]
        self.songName = score_json["songName"]
        self.songSubName = score_json["songSubName"]
        self.songAuthorName = score_json["songAuthorName"]
        self.levelAuthorName = score_json["levelAuthorName"]
        self.difficulty = score_json["difficulty"]
        self.difficultyRaw = score_json["difficultyRaw"]
        self.maxScore = score_json["maxScore"]

    def __str__(self):
        return f"Score {self.songName} ({self.scoreId})"
