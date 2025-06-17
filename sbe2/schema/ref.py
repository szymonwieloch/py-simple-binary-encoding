from .common import FixedLengthElement
from dataclasses import dataclass

@dataclass
class Ref(FixedLengthElement):
    """
    Represents a reference element in the schema.
    This is used to refer to other defined types.
    """
    
    type_name: str
    type_: FixedLengthElement = None  # The type this reference points to. Set lazily
    offset: int|None = None  # Offset in bytes, if applicable
    