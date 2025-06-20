"""Defines a section in the strip.."""

from __future__ import annotations

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin

# TODO: adapt commands to the new format

@dataclass
class Response(DataClassJSONMixin):
    """Base class for all responses (all responses have the same format)."""

    status: int

    command: str | None

    description: str

    data: dict
