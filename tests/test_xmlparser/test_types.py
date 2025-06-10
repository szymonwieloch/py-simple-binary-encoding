from lxml.etree import XML as xml
from sbe2.xmlparser.types import parse_valid_value, parse_enum, parse_choice, parse_set, parse_ref, parse_composite
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


def test_parse_choice():
    node = xml(
        """
    <choice name="TestChoice" sinceVersion="1" deprecated="2" description="Test Choice">6</choice>
    """
    )
    choice = parse_choice(node)
    assert choice.name == "TestChoice"
    assert choice.since_version == 1
    assert choice.deprecated == 2
    assert choice.description == "Test Choice"
    assert choice.value == 6

    with raises(SchemaParsingError):
        node = xml(
            """
        <choice name="TestChoice" sinceVersion="1" deprecated="2" description="Test Choice">invalid</choice>
        """
        )
        parse_choice(node)


def test_parse_set():
    node = xml(
        """
    <set name="TestSet" sinceVersion="1" deprecated="2" description="Test Set" encodingType="int" offset="0">
        <choice name="Value1">1</choice>
        <choice name="Value2">2</choice>
    </set>
    """
    )
    set_ = parse_set(node)
    assert set_.name == "TestSet"
    assert set_.since_version == 1
    assert set_.deprecated == 2
    assert set_.description == "Test Set"
    assert set_.encoding_type == "int"
    assert set_.offset == 0
    assert len(set_.choices) == 2
    assert set_.choices[0].name == "Value1"
    assert set_.choices[0].value == 1
    assert set_.choices[1].name == "Value2"
    assert set_.choices[1].value == 2

    # duplicate names and values should raise an error

    with raises(SchemaParsingError):
        node = xml(
            """
        <set name="TestSet" sinceVersion="1" deprecated="2" description="Test Set" encodingType="int" offset="0">
            <choice name="Value1">2</choice>
            <choice name="Value2">2</choice>
        </set>
        """
        )
        parse_set(node)
    with raises(SchemaParsingError):
        node = xml(
            """
        <set name="TestSet" sinceVersion="1" deprecated="2" description="Test Set" encodingType="int" offset="0">
            <choice name="Value1">1</choice>
            <choice name="Value1">2</choice>
        </set>
        """
        )
        parse_set(node)


def test_parse_ref():
    node = xml(
        """
    <ref name="TestRef" description="Test Reference" type="int" offset="56"/>
    """
    )
    ref = parse_ref(node)
    assert ref.name == "TestRef"
    assert ref.description == "Test Reference"
    assert ref.type_ == "int"
    assert ref.offset == 56

    with raises(SchemaParsingError):
        node = xml(
            """
        <ref name="TestRef" sinceVersion="1" deprecated="2" description="Test Reference"/>
        """
        )
        parse_ref(node)  # type should be mandatory