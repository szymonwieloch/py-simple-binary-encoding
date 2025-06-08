from lxml.etree import XML as xml
from sbe2.xmlparser.types import parse_valid_value, parse_enum
from sbe2.xmlparser.errors import SchemaParsingError
from pytest import raises


def test_parse_valid_value():
    node = xml(
        '<validValue name="something" sinceVersion="5" deprecated="8" description="blah" >5</validValue>'
    )
    vv = parse_valid_value(node)
    assert vv.name == "something"
    assert vv.value == 5
    assert vv.since_version == 5
    assert vv.deprecated == 8
    assert vv.description == "blah"


def test_parse_enum():
    node = xml(
        """
    <enum name="TestEnum" sinceVersion="1" deprecated="2" description="Test Enum" encodingType="int" offset="0">
        <validValue name="Value1">1</validValue>
        <validValue name="Value2">2</validValue>
    </enum>
    """
    )
    enum = parse_enum(node)
    assert enum.name == "TestEnum"
    assert enum.since_version == 1
    assert enum.deprecated == 2
    assert enum.description == "Test Enum"
    assert enum.encoding_type == "int"
    assert enum.offset == 0
    assert len(enum.valid_values) == 2
    assert enum.valid_values[0].name == "Value1"
    assert enum.valid_values[0].value == 1
    assert enum.valid_values[1].name == "Value2"
    assert enum.valid_values[1].value == 2

    # duplicate names and values should raise an error
    with raises(SchemaParsingError):
        node = xml(
            """
        <enum name="TestEnum" sinceVersion="1" deprecated="2" description="Test Enum" encodingType="int" offset="0">
            <validValue name="Value1">2</validValue>
            <validValue name="Value2">2</validValue>
        </enum>
        """
        )
        parse_enum(node)

    with raises(SchemaParsingError):
        node = xml(
            """
        <enum name="TestEnum" sinceVersion="1" deprecated="2" description="Test Enum" encodingType="int" offset="0">
            <validValue name="Value1">1</validValue>
            <validValue name="Value1">2</validValue>
        </enum>
        """
        )
        parse_enum(node)
