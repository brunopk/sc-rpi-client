"""Defines a section in the strip.."""

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin

# TODO: validate color (hexadecimal)  # noqa: FIX002, TD002, TD003

@dataclass
class Section(DataClassJSONMixin):
    """Defines a section in the strip."""

    start: int

    end: int

    color: str
