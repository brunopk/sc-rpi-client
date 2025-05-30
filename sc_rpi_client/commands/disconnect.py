"""disconnect command."""
from dataclasses import dataclass, field

from sc_rpi_client.base_command import BaseCommand


@dataclass
class Disconnect(BaseCommand):
    """Disconnect command."""

    name: str = field(init=False, default="disconnect")
