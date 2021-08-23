from typing import Optional, List

from faker.providers import BaseProvider

from .models import Player, ScoreStats, Score, Characteristic, Difficulty, Badge


class ScoreSaberProvider(BaseProvider):
    def role(self) -> Optional[str]:
        roles = [
            "Owner", "Nomination Assessment Team", "Ranking Team", "Quality Assurance Team",
            "Ranking Team Recruit", "Criteria Assurance Team", "Supporter", None
        ]

        return self.random_choices(roles, 1)

    def rank(self) -> int:
        return self.random_int(1, 1000000000)

    def history(self) -> str:
        ranks = []

        for index in range(48):
            ranks.append(str(self.rank()))

        return ",".join(ranks)

    def badge(self) -> Badge:
        badge = Badge()

        badge.image = self.generator.image_url(80, 30)
        badge.description = self.generator.sentence()

        return badge

    def badges(self) -> List[Badge]:
        badges = []

        rnd = self.random_digit()

        if rnd == 0:
            return badges

        for index in range(rnd):
            badges.append(self.badge())

        return badges

    def player_basic(self, player_id: int) -> Player:
        player = Player()

        player.player_id = player_id
        player.player_name = self.generator.user_name()
        player.avatar = self.generator.image_url(184, 184)
        player.rank = self.rank()
        player.country_rank = self.rank()
        player.pp = float(self.numerify("%####.##"))
        player.country = self.generator.country_code()
        player.role = self.role()
        player.badges = self.badges()
        player.history = self.history()
        player.permissions = self.random_int(0, 100)
        player.inactive = self.random_int(0, 1)
        player.banned = self.random_int(0, 1)

        return player

    def score_stats(self) -> ScoreStats:
        score_stats = ScoreStats()

        score_stats.total_score = self.random_int(0, 999999999999)
        score_stats.total_ranked_score = self.random_int(0, 999999999999)
        score_stats.average_ranked_accuracy = float(self.numerify("%#.##############"))
        score_stats.total_play_count = self.random_int(0, 99999)
        score_stats.ranked_play_count = self.random_int(0, 99999)

        return score_stats

    def player_full(self, player_id: int) -> Player:
        player = self.player_basic(player_id)

        player.score_stats = self.score_stats()

        return player

    def score(self) -> Score:
        score = Score()

        score.rank = self.rank()
        score.score_id = self.random_int(0, 999999999999)
        score.score = self.random_int(0, 999999999999)
        score.unmodified_score = score.score
        score.mods = self.random_elements(["NF", "FS", "SS", "GN"], unique=True)
        score.pp = float(self.numerify("%##.###"))
        score.weight = float(self.numerify("%#.##############"))
        score.time_set = self.generator.past_datetime()
        score.leaderboard_id = self.random_int(0, 999999999999)
        score.song_hash = self.generator.sha1(raw_output=False)
        score.song_name = self.generator.text(35)
        score.song_sub_name = self.generator.text(35)
        score.song_author_name = self.generator.user_name()
        score.level_author_name = self.generator.user_name()
        score.characteristic = self.random_choices(list(Characteristic), 1)
        score.difficulty = self.random_choices(list(Difficulty), 1)
        score.max_score = score.score * float(self.numerify("%.###"))

        return score

    def scores(self, count: int = 1) -> List[Score]:
        scores = []

        for _ in range(count):
            scores.append(self.score())

        return scores

