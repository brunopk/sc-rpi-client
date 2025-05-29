"""Provides methods to interact with sc-rpi.

Based on Based on [WLED API Client for Python](https://pypi.org/project/wled/).
"""

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from exceptions import ScRpiClientError
from typing_extensions import Self

from sc_rpi_client.base_command import BaseCommand
from sc_rpi_client.commands.disconnect import Disconnect

if TYPE_CHECKING:
    import types

    import aiohttp

    from sc_rpi_client.base_command import BaseCommand

LOGGER = getLogger(__package__)

CONNECTION_ERROR_MSG = "_client is None"

class ScRpiClient:
    """Provides methods to interact with sc-rpi."""

    _url: str

    _session: (aiohttp.client.ClientSession)

    _client: (aiohttp.ClientWebSocketResponse | None) = None

    @property
    def _connected(self) -> bool:
        return self._client is not None and not self._client.closed

    async def send_command(self, cmd: BaseCommand) -> None:
        """Send command to device."""
        if self._client is not None:
            cmd_as_dict = cmd.to_dict()
            LOGGER.debug("Sending command %s", cmd_as_dict)
            await self._client.send_json(cmd_as_dict)
        else:
            raise ScRpiClientError(CONNECTION_ERROR_MSG)

    def __init__(self, url: str, session: aiohttp.ClientSession) -> None:
        """Initialize the client."""
        self._url =url
        self._session = session

    async def __aenter__(self) -> Self:
        """Initialize the async context manager."""
        if self._connected:
            return self

        LOGGER.info("Connecting to %s", self._url)
        self._client = await self._session.ws_connect(url=self._url)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        """Finalize the async context manager."""
        if self._session and not self._session.closed:
            await self.send_command(Disconnect())
            LOGGER.info("Closing ClientSession")
            await self._session.close()
        return True
