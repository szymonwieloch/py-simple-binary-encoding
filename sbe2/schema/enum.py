from .common import FixedLengthElement, Element
from .type import Type
from dataclasses import dataclass
from functools import cached_property
from typing import override

@dataclass
class ValidValue(Element):
    """
    Represents a valid value for an enumeration.
    This is used to define the named values in an enum.
    """
    
    value: int | bytes  # The integer or char value associated with this name
    since_version: int = 0  # Version since this value is present
    deprecated: int | None = None  # Version this value was deprecated, if applicable
    enum: 'Enum' = None # set lazily during parsing

@dataclass
class Enum(FixedLengthElement):
    """
    Represents an enumeration element in the schema.
    This is used to define a set of named values.
    """
    
    valid_values: list[ValidValue]
    
    encoding_type_name: str # The name of encoding type for the enum values
    encoding_type:Type = None # The encoding type for the enum values. Set lazily.
    since_version: int = 0  # Version since this enum is present
    deprecated: int|None = None  # Version this enum was deprecated, if applicable  
    offset: int|None = None  # Offset in bytes, if applicable
    
    @cached_property
    @override
    def total_length(self):
        return self.encoding_type.total_length
    
    @override
    def lazy_bind(self, types):
        self.encoding_type = types[self.encoding_type_name]