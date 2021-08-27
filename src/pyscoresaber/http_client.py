import asyncio
import logging
from asyncio import AbstractEventLoop
from typing import Optional

import aiohttp
from aiohttp import ClientResponse, ClientResponseError

from .errors import ScoreSaberException, NotFoundException, ServerException


class HttpClient:
    RETRIES = 10

    def __init__(self, loop: Optional[AbstractEventLoop] = None):
        self.loop = loop
        self._aiohttp = None

    async def start(self):
        if self._aiohttp is None:
            self._aiohttp = aiohttp.ClientSession(loop=self.loop, raise_for_status=True)

    async def close(self):
        if self._aiohttp is not None:
            await self._aiohttp.close()
            self._aiohttp = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _request(self, *args, **kwargs) -> ClientResponse:
        retries = 0

        while True:
            try:
                response = await self._aiohttp.request(*args, **kwargs)

                if response.status == 200:
                    return response

                raise ScoreSaberException(response.status, str(response.real_url))
            except ClientResponseError as error:
                if error.status == 404:
                    raise NotFoundException(error.status, str(error.request_info.real_url)) from error
                elif error.status == 500:
                    raise ServerException(error.status, str(error.request_info.real_url)) from error
                else:
                    if retries > self.RETRIES:
                        raise ScoreSaberException(error.status, str(error.request_info.real_url)) from error

            sleep = 2 ** retries

            logging.warning(f"[{retries}/{self.RETRIES}] Rate limited! Waiting {sleep} seconds...")
            await asyncio.sleep(sleep)

            retries += 1

    async def get(self, type_, url, *args, **kwargs):
        response = await self._request('GET', url, *args, **kwargs)
        data = await response.json()
        return type_.from_dict(data)
