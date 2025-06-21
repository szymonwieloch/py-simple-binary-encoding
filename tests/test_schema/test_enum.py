from sbe2.schema import Enum, Types
from sbe2.schema import builtin
from unittest.mock import MagicMock


def test_enum_lazy_bind():
    enum = Enum(name="TestEnum", encoding_type_name="int", description="", valid_values=[])
    types = Types()
    enum.lazy_bind(types)
    assert enum.encoding_type is builtin.int_
    
    
def test_enum_total_length():
    enum = Enum(name="TestEnum", encoding_type_name="int", description="", valid_values=[], encoding_type=builtin.int_)
    assert enum.total_length == builtin.int_.total_length