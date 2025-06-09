from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar

@dataclass
class PrimitiveType:
    """
    Represents a primitive type built into SBE.
    """
    name: str  # Name of the primitive type
    length: int  # Length of the primitive type in bytes
    max_value: int | float | str  # Maximum value for the primitive type
    min_value: int | float | str  # Minimum value for the primitive type
    default_null_value: int | float | str  # Default null value for the primitive type
    
    by_name: ClassVar[dict[str, "PrimitiveType"]] = {}

    @cached_property
    def is_byte(self) -> bool:
        """
        Returns True if this primitive type is a byte.
        """
        return self.length
    
    
    
    def __post_init__(self):
        """
        Post-initialization to register the primitive type by its name.
        """
        if self.name in PrimitiveType.by_name:
            raise ValueError(f"Primitive type '{self.name}' is already registered.")
        PrimitiveType.by_name[self.name] = self

