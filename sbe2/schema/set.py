from dataclasses import dataclass
from .type import Type

from .common import Element

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
class Set(Element):
    """Represents a set element in the schema.
    This is used to define a collection of choices that can be selected.
    """
    
    encoding_type_name: str
    choices: list[Choice]
    encoding_type: Type = None # Set lazily
    offset: int | None = None
    since_version: int = 0
    deprecated: int | None = None