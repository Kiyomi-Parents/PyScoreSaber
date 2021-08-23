import asyncio
import logging

import aiohttp
from aiohttp import ClientResponse, ClientResponseError

from .errors import ScoreSaberException, NotFoundException, ServerException


class HttpClient(aiohttp.ClientSession):
    RETRIES = 10

    def __init__(self, *args, **kwargs):
        super().__init__(raise_for_status=True, *args, **kwargs)

    async def _request(self, *args, **kwargs) -> ClientResponse:
        retries = 0

        while True:
            try:
                response = await super()._request(*args, **kwargs)
            except ClientResponseError as error:
                if error.status == 404:
                    raise NotFoundException(error.status, str(error.request_info.real_url)) from error
                elif error.status == 500:
                    raise ServerException(error.status, str(error.request_info.real_url)) from error

                raise ScoreSaberException(error.status, str(error.request_info.real_url)) from error

            if response.status == 200:
                return response

            if retries > self.RETRIES:
                raise ScoreSaberException(response.status, str(response.real_url))

            sleep = 2 ** retries

            logging.warning(f"[{retries}/{self.RETRIES}] Ratelimited! Waiting {sleep} seconds...")
            await asyncio.sleep(sleep)

            retries += 1

    async def get(self, url, *args, **kwargs):
        response = await self._request('GET', url, *args, **kwargs)
        return await response.json()
