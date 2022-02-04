import asyncio

import pytest

from pyscoresaber import ScoreSaberAPI


@pytest.yield_fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def scoresaber(event_loop):
    scoresaber = ScoreSaberAPI(loop=event_loop)
    await scoresaber.start()

    yield scoresaber

    await scoresaber.close()

