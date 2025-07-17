from sbe2.backcheck.compare import compare_choice, compare_valid_value
from sbe2.backcheck.errors import Diff, Error
from sbe2.schema import Choice, ValidValue
from copy import deepcopy
from unittest.mock import patch


def test_compare_choice():
    old = Choice(name='TestChoice', description='description', value=6)
    new = deepcopy(old)
    
    diffs = compare_choice(old, new, None)
    assert len(diffs) == 0
    
    with patch.object(new, 'name', new='NewName'):
        diffs = compare_choice(old, new, None)
        assert len(diffs) == 1
        assert diffs[0].error == Error.CHOICE_NAME_MISMATCH
        assert diffs[0].message == 'Choice names do not match: TestChoice != NewName'
        
    with patch.object(new, 'since_version', new=5):
        diffs = compare_choice(old, new, None)
        assert len(diffs) == 1
        assert diffs[0].error == Error.CHOICE_SINCE_VERSION_MISMATCH
        assert diffs[0].message == 'Choice since versions do not match: 0 != 5'
        
    with patch.object(new, 'deprecated', new=5):
        diffs = compare_choice(old, new, None)
        assert len(diffs) == 1
        assert diffs[0].error == Error.CHOICE_DEPRECATED_MISMATCH
        assert diffs[0].message == 'Choice deprecated versions do not match: None != 5'
        
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
        assert diffs[0].message == 'Valid value names do not match: TestValidValue != NewName'
        
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
