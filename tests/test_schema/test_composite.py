from unittest.mock import MagicMock
from sbe2.schema import Composite

def test_composite_lazy_bind():
    mock_type1 = MagicMock()
    mock_type2 = MagicMock()
    composite = Composite(
        name="TestComposite",
        description="",
        elements=[
            mock_type1,
            mock_type2,
        ]
    )
    
    composite.lazy_bind(MagicMock())
    mock_type1.lazy_bind.assert_called_once()
    mock_type2.lazy_bind.assert_called_once()
    
    
def test_composite_total_length():
    mock_type1 = MagicMock()
    mock_type2 = MagicMock()
    mock_type1.total_length = 4  # Simulating an int type
    mock_type2.total_length = 8  # Simulating a double type
    composite = Composite(
        name="TestComposite",
        description="",
        elements=[
            mock_type1,
            mock_type2,
        ]
    )
    assert composite.total_length == 12  # int (4) + double (8) = 12 bytes