"""Provides methods to interact with sc-rpi.

Based on Based on [WLED API Client for Python](https://pypi.org/project/wled/).
"""

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

import aiohttp
from typing_extensions import Self

from sc_rpi_client.commands.base_command import BaseCommand
from sc_rpi_client.commands.disconnect import Disconnect
from sc_rpi_client.commands.section_add import SectionAdd, SectionAddParameters
from sc_rpi_client.exceptions.sc_rpi_client_error import ScRpiClientError

if TYPE_CHECKING:
    import types

    from sc_rpi_client.commands.base_command import BaseCommand
    from sc_rpi_client.models import Section

LOGGER = getLogger(__package__)

CONNECTION_ERROR_MSG = "_client is None"

class ScRpiClient:
    """Provides methods to interact with sc-rpi."""

    def __init__(self, url: str) -> None:
        """Initialize the client."""
        self._url =url
        self._session : aiohttp.ClientSession | None = None

    async def __aenter__(self) -> Self:
        """Initialize the async context manager."""
        LOGGER.info("Connecting to %s", self._url)
        self._session = aiohttp.ClientSession()
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
            await self._send_command(Disconnect())
            LOGGER.info("Closing ClientSession")
            await self._session.close()
        return True

    async def section_add(self, sections: list[Section]) -> None:
        """section_add command."""
        cmd = SectionAdd(SectionAddParameters(sections))
        await self._send_command(cmd)

    async def _send_command(self, cmd: BaseCommand) -> None:
        """Send command to device."""
        if self._client is not None:
            cmd_as_dict = cmd.to_dict()
            LOGGER.debug("Sending command %s", cmd_as_dict)
            await self._client.send_json(cmd_as_dict)
        else:
            raise ScRpiClientError(CONNECTION_ERROR_MSG)
