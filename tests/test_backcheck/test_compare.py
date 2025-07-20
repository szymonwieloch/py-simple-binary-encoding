from sbe2.backcheck.compare import compare_choice, compare_valid_value, type_name, match_by_value, check_common
from sbe2.backcheck.errors import Diff, Error
from sbe2.schema import Choice, ValidValue, Set, Enum, Composite, Type, Presence, primitive_type
from copy import deepcopy
from unittest.mock import patch, MagicMock


def test_compare_choice():
    old = Choice(name='TestChoice', description='description', value=6)
    new = deepcopy(old)
    
    diffs = compare_choice(old, new, None)
    assert len(diffs) == 0
    
    with patch.object(new, 'name', new='NewName'):
        diffs = compare_choice(old, new, None)
        assert len(diffs) == 1
        assert diffs[0].error == Error.CHOICE_NAME_MISMATCH
        assert diffs[0].message == 'Choice TestChoice name does not match: TestChoice != NewName'
        
    with patch.object(new, 'since_version', new=5):
        diffs = compare_choice(old, new, None)
        assert len(diffs) == 1
        assert diffs[0].error == Error.CHOICE_SINCE_VERSION_MISMATCH
        assert diffs[0].message == 'Choice TestChoice since versions do not match: 0 != 5'
        
    with patch.object(new, 'deprecated', new=5):
        diffs = compare_choice(old, new, None)
        assert len(diffs) == 1
        assert diffs[0].error == Error.CHOICE_DEPRECATED_MISMATCH
        assert diffs[0].message == 'Choice TestChoice deprecated versions do not match: None != 5'
        
    with patch.object(new, 'deprecated', new=5):
        diffs = compare_choice(old, new, 5)
        assert len(diffs) == 0
        
        
def test_compare_valid_value():
    old = ValidValue(name='TestValidValue', description='description', value=6)
    new = deepcopy(old)
    
    diffs = compare_valid_value(old, new, None)
    assert len(diffs) == 0
    
    with patch.object(new, 'name', new='NewName'):
        diffs = compare_valid_value(old, new, None)
        assert len(diffs) == 1
        assert diffs[0].error == Error.VALID_VALUE_NAME_MISMATCH
        assert diffs[0].message == 'Valid value TestValidValue name does not match: TestValidValue != NewName'
        
    with patch.object(new, 'since_version', new=5):
        diffs = compare_valid_value(old, new, None)
        assert len(diffs) == 1
        assert diffs[0].error == Error.VALID_VALUE_SINCE_VERSION_MISMATCH
        assert diffs[0].message == 'Valid value TestValidValue since versions do not match: 0 != 5'
        
    with patch.object(new, 'deprecated', new=5):
        diffs = compare_valid_value(old, new, None)
        assert len(diffs) == 1
        assert diffs[0].error == Error.VALID_VALUE_DEPRECATED_MISMATCH
        assert diffs[0].message == 'Valid value TestValidValue deprecated versions do not match: None != 5'
        
    with patch.object(new, 'deprecated', new=5):
        diffs = compare_valid_value(old, new, 5)
        assert len(diffs) == 0


def test_type_name():
    e = Enum(name="TestEnum", description='', valid_values=[], encoding_type_name="blah")
    assert type_name(e) == 'Enum'
    vv = ValidValue(name='TestValidValue', description='', value=1)
    assert type_name(vv) == 'Valid value'
    
    
def test_match_by_value():
    v1 = MagicMock(value=1)
    v2_1 = MagicMock(value=2)
    v2_2 = MagicMock(value=2)
    v3 = MagicMock(value=3)
    
    matched, missing, added = match_by_value([v1, v2_1], [v2_2, v3])
    assert matched == [(v2_1, v2_2)]
    assert missing == [v1]
    assert added == [v3]
    
    
def test_check_common():
    old = Type("TestType", description='', presence=Presence.REQUIRED, primitive_type=primitive_type.uint16, since_version=5)
    new = Type("TestType", description='', presence=Presence.REQUIRED, primitive_type=primitive_type.uint16, since_version=5)
    
    def check_v(new_version:int|None=None) -> list[Error]:
        return [diff.error for diff in check_common(old, new, new_version)]
    
    assert check_v() == []
    assert check_v(10) == []
    
    with patch.object(new, 'deprecated', new=8):
        assert check_v(8) == []
        assert check_v() == [Error.TYPE_DEPRECATED_MISMATCH]
        assert check_v(9) == [Error.TYPE_DEPRECATED_MISMATCH]
    
    with patch.object(new, 'since_version', new=7):
        assert check_v() == [Error.TYPE_SINCE_VERSION_MISMATCH]
        
    with patch.object(new, 'name', new="OtherName"):
        assert check_v() == [Error.TYPE_NAME_MISMATCH]