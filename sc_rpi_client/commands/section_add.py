"""section_add command."""
from dataclasses import dataclass, field

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi_client.commands.base_command import Command
from sc_rpi_client.models.section import Section


@dataclass
class SectionAddParameters(DataClassJSONMixin):
    """section_add command parameters."""

    sections: list[Section] = field(default_factory=list)

@dataclass
class SectionAdd(Command):
    """section_add command."""

    name: str = field(default="section_add", init=False)

    args: SectionAddParameters
