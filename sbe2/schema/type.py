from .common import FixedLengthElement, Presence
from .primitive_type import PrimitiveType
from dataclasses import dataclass
from functools import cached_property
from typing import Any, override



# TODO: move

def value_ref_to_valid_value(value_ref:str, types):
    from .enum import Enum
    enum_name, valid_value = value_ref.split('.')
    enum = types[enum_name]
    if not isinstance(enum, Enum):
        raise ValueError(f"'{enum_name}' type is not enum")
    for vv in enum.valid_values:
        if vv.name == valid_value:
            return vv
    raise ValueError(f"Enum '{enum_name}' does not contain value '{valid_value}'")

@dataclass
class Type(FixedLengthElement):
    """
    Represents a type element in the schema.
    This is used to define a specific type of data.
    """
    
    presence: Presence
    primitive_type: PrimitiveType
    length: int = 1  # Length of an array, by default just one element
    offset: int | None = None # Offset in bytes, if applicable
    since_version: int = 0  # Version since this type is present
    deprecated: int | None = None  # Version this type was deprecated, if applicable
    value_ref: str | None = None # constant value reference
    value: str | None = None # constant value of the given field
    const_val: Any = None # constant value translated into Python type
    
    def lazy_bind(self, types):
        if self.presence is Presence.CONSTANT and self.const_val is None:
            if self.value_ref:
                vv = value_ref_to_valid_value(self.value_ref, types)
                self.const_val = vv.value
            elif self.value:
                self.const_val = self.parse(self.value)
            else:
                raise ValueError(f"Type '{self.name}' is constant but does not have any constant value assigned")
    
    @cached_property
    @override
    def total_length(self):
        if self.presence is Presence.CONSTANT:
            return 0
        return self.primitive_type.length
    
    
    @override
    def parse(self, val: str):
        if self.length == 1:
            return self.primitive_type.base_type(val)
        raise NotImplementedError