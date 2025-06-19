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
    value_ref: str | None = None # constant value reference
    const_val: str | None = None # constant value
    
    @cached_property
    def total_length(self):
        return self.primitive_type.length
    
    def parse(self, val: str):
        if self.length == 1:
            return self.primitive_type.base_type(val)
        raise NotImplementedError