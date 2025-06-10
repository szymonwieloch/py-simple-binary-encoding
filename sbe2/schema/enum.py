from .common import FixedLengthElement, Element
from dataclasses import dataclass

@dataclass
class ValidValue(Element):
    """
    Represents a valid value for an enumeration.
    This is used to define the named values in an enum.
    """
    
    value: int  # The integer value associated with this name
    since_version: int = 0  # Version since this value is present
    deprecated: int | None = None  # Version this value was deprecated, if applicable

@dataclass
class Enum(FixedLengthElement):
    """
    Represents an enumeration element in the schema.
    This is used to define a set of named values.
    """
    
    valid_values: list[ValidValue]
    encoding_type:str # The encoding type for the enum values
    since_version: int = 0  # Version since this enum is present
    deprecated: int|None = None  # Version this enum was deprecated, if applicable  
    offset: int|None = None  # Offset in bytes, if applicable