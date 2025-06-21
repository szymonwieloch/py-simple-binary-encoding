from .common import FixedLengthElement, Presence
from dataclasses import dataclass
from functools import cached_property
from typing import Any


@dataclass
class Field(FixedLengthElement):
    """
    Represents a field in the SBE schema.
    """

    id: int
    type: FixedLengthElement
    offset: int | None = None
    alignment: int | None = None
    presence: Presence = Presence.REQUIRED
    value_ref: Any = None
    constant_value: Any = None
    since_version: int = 0
    deprecated: int | None = None

    @cached_property
    def total_length(self) -> int:
        """
        Returns the total length of the field, which is the size of the type.
        """
        return self.type.total_length
