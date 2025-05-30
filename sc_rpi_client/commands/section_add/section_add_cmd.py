"""section_add command."""
from dataclasses import dataclass, field

from sc_rpi_client.base_command import BaseCommand
from sc_rpi_client.commands.section_add.section_add_params import (
    SectionAddParams,
)


@dataclass
class SectionAdd(BaseCommand):
    """section_add command."""

    name: str = field(default="section_add", init=False)

    args: SectionAddParams
