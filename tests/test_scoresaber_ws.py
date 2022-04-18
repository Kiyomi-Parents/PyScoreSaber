from src.pyscoresaber import ScoreSaber


async def test_websocket_live_feed(scoresaber: ScoreSaber):
    await scoresaber.ws_start()
    score_count = 0
    async for playerScore in scoresaber.websocket():

        assert playerScore.score.id is not None
        assert playerScore.leaderboard.id is not None

        score_count += 1

        if score_count > 5:
            await scoresaber.ws_close()
