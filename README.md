[![PyPI version](https://badge.fury.io/py/PyScoreSaber.svg)](https://pypi.org/project/PyScoreSaber)
# PyScoreSaber
Score Saber API client

### Usage:
```python
import asyncio
from pyscoresaber import ScoreSaber


async def main():
    async with ScoreSaber() as scoresaber:
        player = await scoresaber.get_player_full("76561198029447509")
        print(player)


asyncio.run(main())
```
