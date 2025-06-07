"""Defines a section in the strip.."""

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class Response(DataClassJSONMixin):
    """Base class for all responses (all responses have the same format)."""

    status: int

    description: str

    data: dict
