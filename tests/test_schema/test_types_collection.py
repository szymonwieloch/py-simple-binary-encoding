from sbe2.schema import Types, Enum
from sbe2.schema.builtin import decimal, decimal32, decimal64,primitive_type_to_type, int_
from pytest import raises


def test_types_initialization():
    types_ =Types()
    assert len(types_) > 0
    
    assert types_['decimal'] == decimal
    assert types_['decimal32'] == decimal32
    assert types_['decimal64'] == decimal64
    assert types_['int'] == primitive_type_to_type(int_)
    
    
def test_types_get():
    types_ = Types()
    assert types_['decimal'] == decimal
    
    with raises(KeyError):
        _ = types_['non_existent_type']
        
def test_types_add():
    types_ = Types()
    new_type = Enum(name="NewType", encoding_type="int", description="", valid_values=[])
    types_.add(new_type)
    
    assert len(types_) > 0
    assert types_[new_type.name] == new_type
    
    with raises(ValueError):
        types_.add(new_type)
    # Attempting to add a type with the same name should raise ValueError
        with raises(ValueError):
            types_.add(new_type)
            
        got = types_['NewType']
        assert got == new_type