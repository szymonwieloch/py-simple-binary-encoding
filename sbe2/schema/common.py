import enum
from dataclasses import dataclass

class Presence(enum.StrEnum):
    'Matches the `presence` attribute in the schema.'
    REQUIRED = "required"
    OPTIONAL = "optional"
    CONSTANT = "constant"

class ByteOrder(enum.StrEnum):
    'Matches the `byteOrder` attribute in the schema.'
    BIG_ENDIAN = "bigEndian"
    LITTLE_ENDIAN = "littleEndian"

@dataclass
class Element:
    name: str
    description: str
    
    
@dataclass
class FixedLengthElement(Element):
    """
    Represents an element with a fixed length in bytes.
    This is a base class for elements that have a defined size.
    """
   
    @property
    def total_length(self) -> int:
        """
        Returns the total length of the element in bytes.
        This is a placeholder and should be overridden in subclasses.
        """
        raise NotImplementedError("Subclasses must implement total_length")
