"""`disconnect` command."""
from dataclasses import dataclass, field

from sc_rpi_client.commands.base_command import Command

DISCONNECT = "disconnect"

@dataclass
class Disconnect(Command):
    """`disconnect` command."""

    name: str = field(init=False, default=DISCONNECT)
