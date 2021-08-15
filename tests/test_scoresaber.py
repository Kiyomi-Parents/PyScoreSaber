from unittest import IsolatedAsyncioTestCase

from src.pyscoresaber import NotFoundException
from src.pyscoresaber.scoresaber import ScoreSaber


class TestScoreSaber(IsolatedAsyncioTestCase):
    valid_player_id = "76561198029447509"
    invalid_player_id = "656119802447509"

    def setUp(self):
        self.scoresaber = ScoreSaber()

    async def test_get_player_basic_valid(self):
        player = await self.scoresaber.get_player_basic(self.valid_player_id)
        self.assertTrue(player.player_id == self.valid_player_id)

    async def test_get_player_basic_invalid(self):
        with self.assertRaises(NotFoundException):
            await self.scoresaber.get_player_basic(self.invalid_player_id)

    async def test_get_player_full_valid(self):
        player = await self.scoresaber.get_player_full(self.valid_player_id)
        self.assertTrue(player.player_id == self.valid_player_id)

    async def test_get_player_full_invalid(self):
        with self.assertRaises(NotFoundException):
            await self.scoresaber.get_player_full(self.invalid_player_id)

    async def test_get_recent_scores_valid(self):
        scores = await self.scoresaber.get_recent_scores(self.valid_player_id)
        self.assertGreater(len(scores), 0)

    async def test_get_recent_scores_invalid(self):
        with self.assertRaises(NotFoundException):
            await self.scoresaber.get_recent_scores(self.invalid_player_id)

    async def test_get_top_scores_valid(self):
        scores_1 = await self.scoresaber.get_top_scores(self.valid_player_id, 1)
        self.assertGreater(len(scores_1), 0)

        scores_2 = await self.scoresaber.get_top_scores(self.valid_player_id, 2)
        self.assertGreater(len(scores_2), 0)

    async def test_get_top_scores_invalid(self):
        with self.assertRaises(NotFoundException):
            await self.scoresaber.get_top_scores(self.invalid_player_id, 1)

        with self.assertRaises(NotFoundException):
            await self.scoresaber.get_top_scores(self.invalid_player_id, 2)

    async def test_get_top_scores_invalid_page(self):
        scores_1 = await self.scoresaber.get_top_scores(self.valid_player_id, 1)
        self.assertGreater(len(scores_1), 0)

        with self.assertRaises(NotFoundException):
            await self.scoresaber.get_top_scores(self.valid_player_id, 12412312)
