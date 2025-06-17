from .common import FixedLengthElement, Presence
from .primitive_type import PrimitiveType
from dataclasses import dataclass
from functools import cached_property

@dataclass
class Type(FixedLengthElement):
    """
    Represents a type element in the schema.
    This is used to define a specific type of data.
    """
    
    presence: Presence
    primitive_type: PrimitiveType
    length: int = 1  # Length of an array, by default just one element
    offset: int | None = None # Offset in bytes, if applicable
    since_version: int = 0  # Version since this type is present
    deprecated: int | None = None  # Version this type was deprecated, if applicable
    
    @cached_property
    def total_length(self):
        return self.primitive_type.length