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
    base_type: type # Python type equivalent
    
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


char = PrimitiveType(name='char', length=1, max_value=126, min_value=26, default_null_value=0, base_type=str)
int_ = PrimitiveType(name='int', length=4, max_value=2**31-1, min_value=-(2**31-1), default_null_value=-(2**31), base_type=int)
int8 = PrimitiveType(name='int8', length=1, max_value=127, min_value=-127, default_null_value=-128, base_type=int)
int16 = PrimitiveType(name='int16', length=2, max_value=(2**15-1), min_value=-(2**15-1), default_null_value=-(2**15), base_type=int)
int32 = PrimitiveType(name='int32', length=4, max_value=(2**31-1), min_value=-(2**31-1), default_null_value=-(2**31), base_type=int)
int64 = PrimitiveType(name='int64', length=8, max_value=(2**63-1), min_value=-(2**63-1), default_null_value=-(2**63), base_type=int)
uint8 = PrimitiveType(name='uint8', length=1, max_value=2**8-2, min_value=0, default_null_value=2**8-1, base_type=int)
uint16 = PrimitiveType(name='uint16', length=2, max_value=2**16-2, min_value=0, default_null_value=2**16-1, base_type=int)
uint32 = PrimitiveType(name='uint32', length=4, max_value=2**32-2, min_value=0, default_null_value=2**32-1, base_type=int)
uint64 = PrimitiveType(name='uint64', length=8, max_value=2**64-2, min_value=0, default_null_value=2**64-1, base_type=int)
float_ = PrimitiveType(name='float', length=4, max_value=float('inf'), min_value=-float('inf'), default_null_value=float('nan'), base_type=float)
double = PrimitiveType(name='double', length=8, max_value=float('inf'), min_value=-float('inf'), default_null_value=float('nan'), base_type=float)