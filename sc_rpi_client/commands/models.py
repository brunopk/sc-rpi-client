"""Models that are used in different commands."""

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class Section(DataClassJSONMixin):
    """Defines a section in the strip."""

    start: int

    end: int

    color: str
