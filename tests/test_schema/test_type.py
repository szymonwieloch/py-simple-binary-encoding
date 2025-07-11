from sbe2.schema import Type, Presence, Enum, ValidValue, Types
from sbe2.schema.primitive_type import double, int_, int16
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
        
def test_type_effective_null_value():
    t1 = Type(name="TestType", description="", primitive_type=double, presence=Presence.OPTIONAL, null_value=0.0)
    assert t1.effective_null_value == 0.0
    
    t2 = Type(name="TestType", description="", primitive_type=double, presence=Presence.OPTIONAL)
    assert t2.effective_null_value is double.default_null_value  # Should match the default null value for double
    
    t3 = Type(name="TestType", description="", primitive_type=double, presence=Presence.REQUIRED, null_value=0.0)
    assert t3.effective_null_value is None
    
def test_type_effective_max_value():
    t1 = Type(name="TestType", description="", primitive_type=int16, presence=Presence.REQUIRED, max_value=5)
    assert t1.effective_max_value == 5
    
    t2 = Type(name="TestType", description="", primitive_type=int16, presence=Presence.REQUIRED)
    assert t2.effective_max_value == int16.max_value  # Should match the default max value for int16
    
    
def test_type_effective_min_value():
    t1 = Type(name="TestType", description="", primitive_type=int16, presence=Presence.REQUIRED, min_value=5)
    assert t1.effective_min_value == 5
    
    t2 = Type(name="TestType", description="", primitive_type=int16, presence=Presence.REQUIRED)
    assert t2.effective_min_value == int16.min_value  # Should match the default min value for int16