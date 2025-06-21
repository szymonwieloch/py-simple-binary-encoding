from sbe2.schema import Set, Types
from sbe2.schema import builtin

def test_set_lazy_bind():
    s = Set(name="TestSet", description="", encoding_type_name="int", choices=[])
    types = Types()
    assert s.encoding_type is None  # Initially, type should be None
    s.lazy_bind(types)
    assert s.encoding_type is builtin.int_
    
    
def test_set_total_length():
    s = Set(name="TestSet", description="", encoding_type_name="int", encoding_type=builtin.int_, choices=[])
    assert s.total_length == builtin.int_.total_length  # Should match the total length of the int type