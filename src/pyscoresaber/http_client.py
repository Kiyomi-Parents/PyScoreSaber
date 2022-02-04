import asyncio
import logging
import typing
from asyncio import AbstractEventLoop
from datetime import datetime
from enum import Enum
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

                if error.status == 500:
                    raise ServerException(error.status, str(error.request_info.real_url)) from error

                if retries > self.RETRIES:
                    raise ScoreSaberException(error.status, str(error.request_info.real_url)) from error

            sleep = 2 ** retries

            logging.warning(f"[{retries}/{self.RETRIES}] Rate limited! Waiting {sleep} seconds...")
            await asyncio.sleep(sleep)

            retries += 1

    def _format_params(self, params):

        for key, value in params.copy().items():
            if value is None:
                del params[key]
                continue

            params[key] = self._format_value(value)

        return params

    @staticmethod
    def _format_value(value):
        if isinstance(value, datetime):
            return 1000 * int(value.timestamp())

        if isinstance(value, Enum):
            return value.value

        return value

    async def get(self, type_, url, params={}, *args, **kwargs):
        params = self._format_params(params)

        response = await self._request('GET', url, params=params, *args, **kwargs)
        data = await response.json()

        if not typing.get_args(type_):
            if isinstance(data, int):
                return data

            return type_.from_dict(data)

        return typing.get_args(type_)[0].schema().load(data, many=True)
