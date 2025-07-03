from .common import FixedLengthElement, TypeKind
from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar

@dataclass
class Ref(FixedLengthElement):
    """
    Represents a reference element in the schema.
    This is used to refer to other defined types.
    """
    
    type_name: str
    type_: FixedLengthElement = None  # The type this reference points to. Set lazily
    offset: int|None = None  # Offset in bytes, if applicable
    
    type_kind: ClassVar[TypeKind] = TypeKind.REF
    
    @cached_property
    def total_length(self) -> int:
        return self.type_.total_length
    
    
    def lazy_bind(self, types):
        self.type_ = types[self.type_name]
    