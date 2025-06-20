"""Provides methods to interact with sc-rpi.

Based on Based on [WLED API Client for Python](https://pypi.org/project/wled/).
"""

from __future__ import annotations

import asyncio
from logging import Logger, getLogger
from typing import TYPE_CHECKING

import aiohttp
from typing_extensions import Self

from sc_rpi_client.commands.base_command import Command
from sc_rpi_client.commands.disconnect import Disconnect
from sc_rpi_client.commands.section_add import SectionAdd, SectionAddParameters
from sc_rpi_client.exceptions.sc_rpi_client_error import ScRpiClientError
from sc_rpi_client.response import Response
import contextlib

if TYPE_CHECKING:
    import types
    from collections.abc import Awaitable
    from typing import Callable

    from sc_rpi_client.commands.base_command import Command
    from sc_rpi_client.models import Section

LOGGER = getLogger(__package__)

CONNECTION_ERROR_MSG = "self._ws is None"

class ScRpi:
    """Provides methods to interact with sc-rpi.

    Based on Based on [WLED API Client for Python](https://pypi.org/project/wled/).
    """

    def __init__(
        self,
        url: str,
        on_message: Callable[[Response], Awaitable[None]] | None = None,
        log: Logger = LOGGER,
    ) -> None:
        """Initialize the client."""
        self._url =url
        self._on_message = on_message
        self._log = log
        self._ws_lock = asyncio.Lock()
        self._session : aiohttp.ClientSession | None = None

    async def __aenter__(self) -> Self:
        """Initialize the async context manager."""
        self._log.info("Connecting to %s", self._url)
        self._session = aiohttp.ClientSession()
        self._ws = await self._session.ws_connect(url=self._url)
        self._log.debug("Subscribing on_message callback")
        self._listen_task = asyncio.create_task(self._listen_ws())
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        """Finalize the async context manager."""
        if self._session and not self._session.closed:
            await self._send_command(Disconnect())
            self._log.info("Closing ClientSession")
            await self._session.close()
        return True

    async def section_add(self, sections: list[Section]) -> None:
        """`section_add` command."""
        cmd = SectionAdd(SectionAddParameters(sections))
        await self._send_command(cmd)

    async def _send_command(self, cmd: Command) -> None:
        """Send command to device."""
        async with self._ws_lock:
            if self._ws is not None:
                cmd_as_dict = cmd.to_dict()
                self._log.debug("Sending command %s", cmd_as_dict)
                await self._ws.send_json(cmd_as_dict)
            else:
                raise ScRpiClientError(CONNECTION_ERROR_MSG)

    async def _listen_ws(self) -> None:
        print("ENTRANDO _listen_ws")
        try:
            async for msg in self._ws:
                print("LLEGA")
                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        response = msg.json()
                    except Exception as ex:
                        raise ScRpiClientError from ex
                    if self._on_message:
                        await self._on_message(Response.from_json(response))
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
        except Exception:
            LOGGER.exception("Exception listening websocket")
        finally:
            print(f"listen_ws exited, closed={self._ws.closed}, code={self._ws.close_code}")
        print("SALIENDO _listen_ws")

