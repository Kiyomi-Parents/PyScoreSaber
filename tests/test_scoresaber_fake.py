from unittest import IsolatedAsyncioTestCase

from src.pyscoresaber import ScoreSaberAPI


class TestScoreSaberFake(IsolatedAsyncioTestCase):
    valid_player_ids = [
        "76561198029447509",
        "76561198333869741",
        "76561198187936410",
        "76561198835772160",
        "76561197995162898",
        "76561198153101808",
        "2538637699496776"
    ]

    async def asyncSetUp(self):
        self.scoresaber = ScoreSaberAPI(test_mode=True)
        await self.scoresaber.start()

    async def asyncTearDown(self):
        await self.scoresaber.close()

    async def test_get_player_basic_valid(self):
        player = await self.scoresaber.player_basic(self.valid_player_ids[0])
        assert player.player_id == self.valid_player_ids[0]

    async def test_get_player_full_valid(self):
        player = await self.scoresaber.player_full(self.valid_player_ids[0])
        assert player.player_id == self.valid_player_ids[0]

    async def test_get_recent_scores_valid(self):
        scores = await self.scoresaber.player_scores_recent(self.valid_player_ids[0])
        assert len(scores) > 0

    async def test_get_top_scores_valid(self):
        scores_1 = await self.scoresaber.player_scores_top(self.valid_player_ids[0], 1)
        assert len(scores_1) > 0

        scores_2 = await self.scoresaber.player_scores_top(self.valid_player_ids[0], 2)
        assert len(scores_2) > 0

    async def test_players_basic(self):
        async for player in self.scoresaber.players_basic(self.valid_player_ids):
            assert player.player_id in self.valid_player_ids

    async def test_players_full(self):
        async for player in self.scoresaber.players_full(self.valid_player_ids):
            assert player.player_id in self.valid_player_ids

    async def test_player_scores_recent_all(self):
        pages = 0
        async for scores in self.scoresaber.player_scores_recent_all(self.valid_player_ids[0]):
            if pages > 2:
                break

            assert len(scores) > 0
            pages += 1

    async def test_player_scores_top_all(self):
        pages = 0
        async for scores in self.scoresaber.player_scores_top_all(self.valid_player_ids[0]):
            if pages > 2:
                break

            assert len(scores) > 0
            pages += 1
