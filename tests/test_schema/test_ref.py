from sbe2.schema import Ref, Types
from unittest.mock import MagicMock
from sbe2.schema import builtin

def test_ref_lazy_bind():
    ref = Ref(name="TestRef", description="", type_name="int")
    types = Types()
    assert ref.type_ is None  # Initially, type should be None
    ref.lazy_bind(types)
    assert ref.type_ is builtin.int_
    
    
def test_ref_total_length():
    ref = Ref(name="TestRef", description="", type_name="int", type_=builtin.int_)
    assert ref.total_length == builtin.int_.total_length  # Should match the total length of the int type