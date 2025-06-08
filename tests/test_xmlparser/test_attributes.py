from sbe2.xmlparser.attributes import (
    parse_name,
    parse_description,
    parse_since_version,
    parse_deprecated,
    parse_alignment,
    parse_offset,
    parse_block_length,
    parse_id,
    parse_presence,
    parse_semantic_type,
    parse_encoding_type,
)
from sbe2.schema import Presence
from sbe2.xmlparser.errors import SchemaParsingError
from lxml.etree import XML as xml
from pytest import raises


def test_parse_name():
    node = xml("<element name='testName'/>")
    assert parse_name(node) == "testName"
    with raises(SchemaParsingError):
        parse_name(xml("<element/>"))


def test_parse_description():
    node = xml("<element description='This is a test description'/>")
    assert parse_description(node) == "This is a test description"
    assert parse_description(xml("<element/>")) == ""


def test_parse_since_version():
    node = xml("<element sinceVersion='5'/>")
    assert parse_since_version(node) == 5
    assert parse_since_version(xml("<element/>")) == 0


def test_parse_deprecated():
    node = xml("<element deprecated='1'/>")
    assert parse_deprecated(node) == 1
    assert parse_deprecated(xml("<element/>")) is None
    assert parse_deprecated(xml("<element deprecated='0'/>")) == 0
    with raises(SchemaParsingError):
        parse_deprecated(xml("<element deprecated='invalid'/>"))


def test_parse_alignment():
    node = xml("<element alignment='8'/>")
    assert parse_alignment(node) == 8
    assert parse_alignment(xml("<element/>")) is None
    with raises(SchemaParsingError):
        parse_alignment(xml("<element alignment='invalid'/>"))


def test_parse_offset():
    node = xml("<element offset='16'/>")
    assert parse_offset(node) == 16
    assert parse_offset(xml("<element/>")) is None
    with raises(SchemaParsingError):
        parse_offset(xml("<element offset='invalid'/>"))


def test_parse_block_length():
    node = xml("<element blockLength='32'/>")
    assert parse_block_length(node) == 32
    assert parse_block_length(xml("<element/>")) is None
    with raises(SchemaParsingError):
        parse_block_length(xml("<element blockLength='invalid'/>"))


def test_parse_id():
    node = xml("<element id='123'/>")
    assert parse_id(node) == 123
    with raises(SchemaParsingError):
        parse_id(xml("<element/>"))
    with raises(SchemaParsingError):
        parse_id(xml("<element id='invalid'/>"))


def test_parse_presence():
    assert parse_presence(xml("<element presence='optional'/>")) == Presence.OPTIONAL
    assert parse_presence(xml("<element presence='required'/>")) == Presence.REQUIRED
    assert parse_presence(xml("<element presence='constant'/>")) == Presence.CONSTANT
    assert parse_presence(xml("<element/>")) is None
    with raises(SchemaParsingError):
        parse_presence(xml("<element presence='invalid'/>"))


def test_parse_semantic_type():
    node = xml("<element semanticType='price'/>")
    assert parse_semantic_type(node) == "price"
    assert parse_semantic_type(xml("<element/>")) == ""


def test_parse_encoding_type():
    node = xml("<element encodingType='ascii'/>")
    assert parse_encoding_type(node) == "ascii"
    with raises(SchemaParsingError):
        parse_encoding_type(xml("<element />"))