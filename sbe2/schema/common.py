import enum
from dataclasses import dataclass
from typing import ClassVar

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
    
    
    
class TypeKind(enum.StrEnum):
    """
    Represents the kind of type in the schema.
    """
    PRIMITIVE = "primitive"
    ENUM = "enum"
    SET = "set"
    COMPOSITE = "composite"
    TYPE = "type"
    REF = "ref"
    
    
@dataclass
class FixedLengthElement(Element):
    """
    Represents an element with a fixed length in bytes.
    This is a base class for elements that have a defined size.
    """
    
    
    type_kind: ClassVar[TypeKind] = None
   
    @property
    def total_length(self) -> int: # pragma: no cover
        """
        Returns the total length of the element in bytes.
        This is a placeholder and should be overridden in subclasses.
        """
        raise NotImplementedError("Subclasses must implement total_length")
    
    
    def lazy_bind(self, types: 'Types') -> None: # pragma: no cover
        """
        Binds types to other types lazily, so that all types are already defined when this is called.
        This is a placeholder and should be overridden in subclasses.
        """
        raise NotImplementedError("Subclasses must implement lazy_bind")
