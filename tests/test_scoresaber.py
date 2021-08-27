from unittest import IsolatedAsyncioTestCase

from src.pyscoresaber import ScoreSaberAPI, NotFoundException


class TestScoreSaber(IsolatedAsyncioTestCase):
    valid_player_ids = [
        "76561198029447509",
        "76561198333869741",
        "76561198187936410",
        "76561198835772160",
        "76561197995162898",
        "76561198153101808",
        "2538637699496776"
    ]
    invalid_player_id = "656119802447509"

    async def asyncSetUp(self):
        self.scoresaber = ScoreSaberAPI()
        await self.scoresaber.start()

    async def asyncTearDown(self):
        await self.scoresaber.close()

    async def test_players(self):
        players = await self.scoresaber.players()
        assert len(players) > 0

    async def test_player_basic_valid(self):
        player = await self.scoresaber.player_basic(self.valid_player_ids[0])
        assert player.player_id == self.valid_player_ids[0]

    async def test_player_basic_invalid(self):
        with self.assertRaises(NotFoundException):
            await self.scoresaber.player_basic(self.invalid_player_id)

    async def test_player_full_valid(self):
        player = await self.scoresaber.player_full(self.valid_player_ids[0])
        assert player.player_id == self.valid_player_ids[0]

    async def test_player_full_invalid(self):
        with self.assertRaises(NotFoundException):
            await self.scoresaber.player_full(self.invalid_player_id)

    async def test_player_scores_recent_valid(self):
        scores = await self.scoresaber.player_scores_recent(self.valid_player_ids[0])
        assert len(scores) > 0

    async def test_player_scores_recent_invalid(self):
        with self.assertRaises(NotFoundException):
            await self.scoresaber.player_scores_recent(self.invalid_player_id)

    async def test_player_scores_top_valid(self):
        scores_1 = await self.scoresaber.player_scores_top(self.valid_player_ids[0], 1)
        assert len(scores_1) > 0

        scores_2 = await self.scoresaber.player_scores_top(self.valid_player_ids[0], 2)
        assert len(scores_2) > 0

    async def test_player_scores_top_invalid(self):
        with self.assertRaises(NotFoundException):
            await self.scoresaber.player_scores_top(self.invalid_player_id, 1)

        with self.assertRaises(NotFoundException):
            await self.scoresaber.player_scores_top(self.invalid_player_id, 2)

    async def test_player_scores_top_invalid_page(self):
        scores_1 = await self.scoresaber.player_scores_recent(self.valid_player_ids[0], 248)
        assert len(scores_1) > 7

        with self.assertRaises(NotFoundException):
            await self.scoresaber.player_scores_recent(self.valid_player_ids[0], 12412312)

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
