from sbe2.schema import Types, Enum
from sbe2.schema.builtin import decimal, decimal32, decimal64, int_
from pytest import raises


def test_types_initialization():
    types_ =Types()
    assert len(types_) > 0
    
    assert types_['decimal'] == decimal
    assert types_['decimal32'] == decimal32
    assert types_['decimal64'] == decimal64
    assert types_['int'] == int_
    
    
def test_types_get():
    types_ = Types()
    assert types_['decimal'] == decimal
    
    with raises(KeyError):
        _ = types_['non_existent_type']
        
def test_types_add():
    types_ = Types()
    new_type = Enum(name="NewType", encoding_type_name="int", description="", valid_values=[])
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
        
        
def test_iter():
    types = Types()
    assert len(list(types)) == 15
    
    
def test_get_composite_type():
    types = Types()
    assert types.get('int') is not None
    with raises(ValueError):
        types.get_composite('int')
        
    types.get_composite('decimal') is not None
        
def test_get_type():
    types = Types()
    assert types.get('decimal') is not None
    with raises(ValueError):
        assert types.get_type('decimal')
    types.get_type('int') is not None