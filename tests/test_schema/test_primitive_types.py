from sbe2.schema.primitive_type import int8, uint8, uint16, char, int64, float_, double


def test_is_byte():
    assert int8.is_byte is True
    assert uint8.is_byte is True
    assert uint16.is_byte is False
    assert char.is_byte is True
    assert int64.is_byte is False
    assert float_.is_byte is False
    assert double.is_byte is False