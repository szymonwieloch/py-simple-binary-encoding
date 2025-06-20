from dataclasses import dataclass
from .type import Type
from functools import cached_property
from .common import Element, FixedLengthElement

@dataclass
class Choice(Element):
    """
    Represents a choice element in the schema.
    This is used to define a set of alternatives where only one can be selected.
    """
    
    value: int
    since_version: int = 0  # Version since this choice is present
    deprecated: int | None = None  # Version this choice was deprecated, if applicable
    

@dataclass
class Set(FixedLengthElement):
    """Represents a set element in the schema.
    This is used to define a collection of choices that can be selected.
    """
    
    encoding_type_name: str
    choices: list[Choice]
    encoding_type: Type = None # Set lazily
    offset: int | None = None
    since_version: int = 0
    deprecated: int | None = None
    
    
    @cached_property
    def total_length(self) -> int:
        return self.encoding_type.total_length
    
    
    def lazy_bind(self, types):
        self.encoding_type = types[self.encoding_type_name]
    