import asyncio
import json
import logging
import typing
from asyncio import AbstractEventLoop
from datetime import datetime
from enum import Enum
from typing import Optional, AsyncIterable

import aiohttp
from aiohttp import ClientResponse, ClientResponseError, ClientSession, ClientWebSocketResponse, WSMessage

from .errors import ScoreSaberException, NotFoundException
from .version import __version__


class HttpClient:
    _ws_url = "ws://scoresaber.com/ws"
    _headers = {
        'User-Agent': f'PyScoreSaber/{__version__}'
    }
    MAX_TIMEOUT = 60

    def __init__(self, loop: Optional[AbstractEventLoop] = None):
        self.loop = loop
        self._aiohttp: Optional[ClientSession] = None
        self._ws: Optional[ClientWebSocketResponse] = None

    async def start(self):
        if self._aiohttp is None:
            self._aiohttp = aiohttp.ClientSession(loop=self.loop, headers=self._headers, raise_for_status=True)

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

            sleep = 10 * retries

            if sleep > self.MAX_TIMEOUT:
                sleep = 60

            logging.warning(f"Request failed! Waiting {sleep} seconds...")
            await asyncio.sleep(sleep)

            retries += 1

    async def ws_connect(self):
        if self._ws is None:
            self._ws = await self._aiohttp.ws_connect(self._ws_url)

    async def ws_close(self):
        if self._ws is not None:
            await self._ws.close()
            self._ws = None

    async def ws_listen(self) -> AsyncIterable[typing.Dict]:
        if self._ws is None:
            await self.ws_connect()

        async for message in self._ws:
            if message.type == aiohttp.WSMsgType.CLOSE:
                logging.warning(f"Websocket closed! Reconnecting...")
                await self.ws_connect()
            if message.type == aiohttp.WSMsgType.TEXT:
                text = message.data

                if text == "Connected to the ScoreSaber WSS":
                    continue

            yield message.json()

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
