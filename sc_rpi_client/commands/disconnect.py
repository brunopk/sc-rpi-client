"""disconnect command."""
from dataclasses import dataclass, field

from sc_rpi_client.commands.base_command import Command


@dataclass
class Disconnect(Command):
    """Disconnect command."""

    name: str = field(init=False, default="disconnect")
