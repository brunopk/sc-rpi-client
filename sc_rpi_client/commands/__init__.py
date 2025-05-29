"""[sc-rpi commands](https://github.com/brunopk/sc-rpi/blob/master/doc/commands.md)."""

from dataclasses import dataclass, field

from mashumaro.mixins.json import DataClassJSONMixin

from .parameters import SectionAddParameters


@dataclass
class Command(DataClassJSONMixin):
    """Base class for all commands."""

    name: str

@dataclass
class Disconnect(Command):
    """Disconnect command."""

    name: str = field(init=False, default="disconnect")

@dataclass
class SectionAdd(Command):
    """Represent the status command."""

    name: str = field(default="section_add", init=False)

    args: SectionAddParameters


