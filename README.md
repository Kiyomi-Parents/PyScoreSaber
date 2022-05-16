[![GitHub license](https://img.shields.io/github/license/Kiyomi-Parents/PyScoreSaber)](https://github.com/Kiyomi-Parents/PyScoreSaber/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/PyScoreSaber.svg)](https://pypi.org/project/PyScoreSaber)
[![codecov](https://codecov.io/gh/Kiyomi-Parents/PyScoreSaber/branch/master/graph/badge.svg?token=X2LFJL839M)](https://codecov.io/gh/Kiyomi-Parents/PyScoreSaber)
[![PyPI supported Python versions](https://img.shields.io/pypi/pyversions/pyscoresaber.svg)](https://pypi.org/project/PyScoreSaber)
[![PyPI downloads](https://img.shields.io/pypi/dm/pyscoresaber?color=blueviolet&logo=pypi)](https://pypi.org/project/PyScoreSaber)
# PyScoreSaber
Score Saber API wrapper

### Features
* Rate Limit handling
* Query Caching
* Everything is ``async``
* Additional helper methods and async generators
* Faker data provider

The faker data mode can be activated with the following ```scoresaber = ScoreSaber(test_mode=True)```.
This will return random data instead of making API requests to Score Saber.

### Usage:
```python
import asyncio
from pyscoresaber import ScoreSaberAPI


async def main():
    async with ScoreSaberAPI() as scoresaber:
        player = await scoresaber.player_full("76561198029447509")
        print(player)

# Get fake data instead
async def main_fake():
    async with ScoreSaberAPI(test_mode=True) as scoresaber:
        player = await scoresaber.player_basic("76561198029447509")
        print(player)

asyncio.run(main())
asyncio.run(main_fake())
```

### Faker provider:
```python
from faker import Faker
from pyscoresaber import ScoreSaberProvider

faker = Faker()
faker.add_provider(ScoreSaberProvider)

player = faker.player_basic("76561198029447509")
print(player)
```
