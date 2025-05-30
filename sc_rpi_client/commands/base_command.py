"""Base class for all commands."""
from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class BaseCommand(DataClassJSONMixin):
    """Base class for all commands."""

    name: str
