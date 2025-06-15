from dataclasses import dataclass
from .composite import Composite

@dataclass
class Data:
    """
    Represents a data object in the SBE2 schema.
    """
    name: str
    id: int
    type_: Composite
    description: str = ""
    semantic_type: str = ""