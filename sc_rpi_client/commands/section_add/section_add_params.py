"""Parameters for section_add command."""

from dataclasses import dataclass, field

from mashumaro.mixins.json import DataClassJSONMixin

from sc_rpi_client.models.section import Section


@dataclass
class SectionAddParams(DataClassJSONMixin):
    """section_add command parameters."""

    sections: list[Section] = field(default_factory=list)
