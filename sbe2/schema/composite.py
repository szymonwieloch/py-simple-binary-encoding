from .common import Element
from dataclasses import dataclass
from functools import cached_property

@dataclass
class Composite(Element):
    """
    Represents a composite element in the schema.
    """
    
    elements: list[Element] # List of elements contained in this composite
    offset: int|None = None  # Offset in bytes, if applicable
    since_version: int = 0  # Version since this composite is present
    deprecated: int|None = None  # Version this composite was deprecated, if applicable

    @cached_property
    def total_length(self) -> int:
        """
        Returns the total length of the composite in bytes.
        This is the sum of the lengths of all contained elements.
        """
        return sum(element.total_length for element in self.elements)