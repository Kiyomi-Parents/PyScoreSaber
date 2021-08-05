class Player:
    """Player data from ScoreSaber"""

    def __init__(self, player_json):
        self.playerId = player_json["playerId"]
        self.playerName = player_json["playerName"]
        self.avatar = player_json["avatar"]
        self.rank = player_json["rank"]
        self.countryRank = player_json["countryRank"]
        self.pp = player_json["pp"]
        self.country = player_json["country"]
        self.role = player_json["role"]
        self.badges = player_json["badges"]
        self.history = player_json["history"]
        self.permissions = player_json["permissions"]
        self.inactive = player_json["inactive"]
        self.banned = player_json["banned"]
        self.discord_user_id = None

    def __str__(self):
        return f"Player {self.playerName} ({self.playerId})"
