"""Provides methods to interact with sc-rpi.

Based on Based on [WLED API Client for Python](https://pypi.org/project/wled/).
"""

from __future__ import annotations

import asyncio
from asyncio import CancelledError, Event, Lock, create_task, wait_for
from logging import Logger, getLogger
from typing import TYPE_CHECKING

from aiohttp import ClientSession, WSMsgType
from typing_extensions import Self

from sc_rpi_client.commands.base_command import Command
from sc_rpi_client.commands.disconnect import DISCONNECT, Disconnect
from sc_rpi_client.commands.section_add import SectionAdd, SectionAddParameters
from sc_rpi_client.exceptions.sc_rpi_client_error import ScRpiClientError
from sc_rpi_client.response import Response

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
        timeout: int | None = 5,
        log: Logger = LOGGER,
    ) -> None:
        """Initialize the client."""
        self._url =url
        self._on_message = on_message
        self._timeout = timeout
        self._log = log
        self._ws_lock = Lock()
        self._session : ClientSession | None = None
        self._disconnect_event = Event()

    async def __aenter__(self) -> Self:
        """Initialize the async context manager."""
        self._log.info("__aenter__: connecting to %s", self._url)
        self._session = ClientSession()
        self._ws = await self._session.ws_connect(url=self._url)
        self._log.debug("__aenter__: subscribing on_message callback")
        self._listen_task = create_task(self._listen_ws())
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        """Finalize the async context manager and close websocket and session."""
        await self._send_command(Disconnect())

        if self._listen_task.done():
            self._log.debug("__aexit__: _listen_task done")

        try:
            if not self._ws.closed and not self._listen_task.done():
                self._log.debug("__aexit__: waiting for self._disconnect_event")
                await wait_for(self._disconnect_event.wait(), self._timeout)
        except asyncio.TimeoutError as ex:
            self._log.debug(
                "__aexit__: timeout waiting for _disconnect_event :",
                exc_info=ex,
            )

        if not self._listen_task.done():
            try:
                self._log.debug("__aexit__: cancelling _listen_task")
                self._listen_task.cancel()
                await self._listen_task
            except CancelledError as ex:
                self._log.debug(
                    "__aexit__: error cancelling _listen_task :",
                    exc_info=ex,
                )

        if self._ws and not self._ws.closed:
            await self._ws.close()

        if self._session and not self._session.closed:
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
                self._log.debug("Sending command : %s", cmd_as_dict)
                await self._ws.send_json(cmd_as_dict)
            else:
                raise ScRpiClientError(CONNECTION_ERROR_MSG)

    async def _listen_ws(self) -> None:
        try:
            if self._on_message:
                async for msg in self._ws:
                    if msg.type == WSMsgType.TEXT:
                        try:
                            response = Response.from_json(msg.json())
                            if response.command != DISCONNECT:
                                await self._on_message(response)
                            else:
                                self._disconnect_event.set()
                                break
                        except Exception as ex:
                            self._log.debug(
                                "_listen_ws: exception receiving message :", exc_info=ex
                            )
                    elif msg.type == WSMsgType.ERROR:
                        self._log.error("_listen_ws: WSMsgType.ERROR")
                        break
        except Exception as ex:
            LOGGER.debug("_listen_ws: exception listening websocket", exc_info=ex)
        except CancelledError:
            LOGGER.debug("_listen_ws: websocket listener cancelled")
            # re-raise so shutdown handles it
            raise
        finally:
            self._log.info(
                "_listen_ws: finalized self._ws.closed=%s, self._ws.close_code=%d",
                self._ws.closed,
                self._ws.close_code,
            )
