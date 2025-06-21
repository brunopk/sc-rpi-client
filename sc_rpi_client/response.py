"""Defines a section in the strip.."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class Response(DataClassJSONMixin):
    """Base class for all responses (the same format for all commands)."""

    status: int

    command: str | None

    payload: dict[str, Any] | None
