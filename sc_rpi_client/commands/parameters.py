"""Classes that define the parameters for commands."""

from dataclasses import dataclass, field

from mashumaro.mixins.json import DataClassJSONMixin

from .models import Section


@dataclass
class SectionAddParameters(DataClassJSONMixin):
    """Represent the status command."""

    sections: list[Section] = field(default_factory=list)
