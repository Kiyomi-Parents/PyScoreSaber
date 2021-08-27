[![PyPI version](https://badge.fury.io/py/PyScoreSaber.svg)](https://pypi.org/project/PyScoreSaber)
# PyScoreSaber
Score Saber API client

Comes with caching and rate limiting out of the box.

There is also a test mode which can be enabled like this ```scoresaber = ScoreSaber(test_mode=True)```.
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
