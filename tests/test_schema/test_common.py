from sbe2.schema import ByteOrder, Presence
from pytest import raises

def test_parse_byte_order():
    assert ByteOrder("bigEndian") == ByteOrder.BIG_ENDIAN
    assert ByteOrder("littleEndian") == ByteOrder.LITTLE_ENDIAN
    with raises(ValueError):
        ByteOrder("invalidByteOrder")

def test_parse_presence():
    assert Presence("required") == Presence.REQUIRED
    assert Presence("optional") == Presence.OPTIONAL
    assert Presence("constant") == Presence.CONSTANT
    with raises(ValueError):
        Presence("invalidPresence")