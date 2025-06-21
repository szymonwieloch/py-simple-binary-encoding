from sbe2.schema import Type, Presence, Enum, ValidValue, Types
from sbe2.schema.primitive_type import double, int_
from unittest.mock import MagicMock
from pytest import raises


def test_type_total_length():
    type_ = Type(name="TestType", description="", primitive_type=double, presence=Presence.REQUIRED)
    assert type_.total_length == 8  # Should match the total length specified
    
    type_ = Type(name="TestType", description="", primitive_type=double, presence=Presence.CONSTANT)
    assert type_.total_length == 0
    
    
def test_type_lazy_bind_const():
    type_ = Type(name="TestType", description="", primitive_type=double, presence=Presence.CONSTANT, value='1.5')
    types = MagicMock() # not used
    type_.lazy_bind(types)
    assert type_.const_val == 1.5  # Should match the constant value specified
    
def test_type_lazy_bind_value_ref():
    types = Types()
    enum = Enum(name="SomeEnum", description="", encoding_type_name='int', valid_values=[
        ValidValue(name="SomeValue", value=42, description=''),
        ValidValue(name="OtherValue", value=100, description=''),
    ])
    types.add(enum)
    
    type_ = Type(name="TestType", description="", primitive_type=int_, presence=Presence.CONSTANT, value_ref="SomeEnum.SomeValue")
    type_.lazy_bind(types)
    assert type_.const_val == 42  # Should match the value from the enum valid value
    
    with raises(KeyError):
        type_ = Type(name="TestType", description="", primitive_type=int_, presence=Presence.CONSTANT, value_ref="NonExistentEnum.SomeValue")
        type_.lazy_bind(types)
        
    with raises(ValueError):
        type_ = Type(name="TestType", description="", primitive_type=int_, presence=Presence.CONSTANT, value_ref="SomeEnum.NonExistentValue")
        type_.lazy_bind(types)
        
        
def test_type_lazy_bind_no_constant():
    type_ = Type(name="TestType", description="", primitive_type=double, presence=Presence.CONSTANT)
    types = MagicMock()  # not used
    with raises(ValueError):
        type_.lazy_bind(types)
    