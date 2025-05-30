"""section_add command."""
from dataclasses import dataclass, field

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi_client.base_command import BaseCommand
from sc_rpi_client.models.section import Section


@dataclass
class SectionAddParameters(DataClassJSONMixin):
    """section_add command parameters."""

    sections: list[Section] = field(default_factory=list)

@dataclass
class SectionAdd(BaseCommand):
    """section_add command."""

    name: str = field(default="section_add", init=False)

    args: SectionAddParameters
