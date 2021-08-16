import asyncio
import logging
from json import JSONDecodeError

import aiohttp

from .errors import RateLimitedException, NotFoundException, ServerErrorException


class HttpClient:
    WAIT_RATE_LIMIT = 60
    WAIT_SERVER_ERROR = 5

    def __init__(self):
        self.__session = None

    async def start(self):
        if self.__session is None:
            self.__session = aiohttp.ClientSession()

    async def close(self):
        if self.__session:
            await self.__session.close()

    async def request(self, method, url, **kwargs):
        async def attempt():
            async with self.__session.request(method, url, **kwargs) as response:
                self.verify_response(response)
                return await self.get_json(response)

        return await self.request_attempt(attempt)

    @staticmethod
    async def get_json(response):
        try:
            data = await response.json()
        except JSONDecodeError:
            logging.exception("JSONDecodeError, response: %r, response.text: %r", response, response.text)
            data = {"error": "Failed to decode json from scoresaber. Somethings broken."}

        return data

    @staticmethod
    def verify_response(response):
        if response.status == 429:
            raise RateLimitedException(response)

        if 400 <= response.status < 500:
            raise NotFoundException(response)

        if 500 <= response.status < 600:
            raise ServerErrorException(response)

    async def request_attempt(self, func):
        attempt = 0
        attempting = True
        last_exception = None

        while attempting and attempt < 6:
            try:
                result = await func()

                attempting = False
                return result
            except ServerErrorException as error:
                attempt += 1
                logging.info(str(error))
                logging.info(f"Waiting {self.WAIT_SERVER_ERROR} seconds...")
                last_exception = error
                await asyncio.sleep(self.WAIT_SERVER_ERROR)
            except RateLimitedException as error:
                attempt += 1
                logging.info(str(error))
                logging.info(f"Waiting {self.WAIT_RATE_LIMIT} seconds...")
                last_exception = error
                await asyncio.sleep(self.WAIT_RATE_LIMIT)

        if last_exception is not None:
            raise last_exception
