from .common import Element
from dataclasses import dataclass

@dataclass
class Ref(Element):
    """
    Represents a reference element in the schema.
    This is used to refer to other defined types.
    """
    
    type: str  # The type this reference points to
    offset: int|None = None  # Offset in bytes, if applicable