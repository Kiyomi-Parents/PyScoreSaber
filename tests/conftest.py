import asyncio

import pytest

from src.pyscoresaber import ScoreSaberAPI


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def scoresaber(event_loop):
    scoresaber_api = ScoreSaberAPI(loop=event_loop)
    await scoresaber_api.start()

    yield scoresaber_api

    await scoresaber_api.close()
