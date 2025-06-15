from dataclasses import dataclass, field
from ..schema.types import Types

@dataclass
class ParsingContext:
    """
    Represents the context for parsing SBE XML files.
    """
    types: Types = field(default_factory=Types)
    