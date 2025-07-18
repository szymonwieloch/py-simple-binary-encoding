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
    parse_character_encoding,
    parse_max_value,
    parse_min_value,
    parse_null_value,
    parse_value_ref,
    parse_primitive_type,
    parse_type,
    parse_length,
    parse_semantic_version,
    parse_byte_order,
    parse_header_type,
    parse_package,
    parse_version,
    parse_dimension_type
)
from sbe2.schema import Presence, ByteOrder, builtin
from sbe2.xmlparser.errors import SchemaParsingError
from sbe2.xmlparser.ctx import ParsingContext
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
    node = xml("<element encodingType='int'/>")
    assert parse_encoding_type(node) == 'int'
    with raises(SchemaParsingError):
        parse_encoding_type(xml("<element />"))
        
        
def test_character_encoding():
    node = xml("<element characterEncoding='UTF-8'/>")
    assert parse_character_encoding(node) == "UTF-8"
    assert parse_character_encoding(xml("<element/>")) is None


def test_parse_max_value():
    node = xml("<element maxValue='100'/>")
    assert parse_max_value(node) == 100
    assert parse_max_value(xml("<element/>")) is None
    with raises(SchemaParsingError):
        parse_max_value(xml("<element maxValue='invalid'/>"))
        
        
def test_parse_min_value():
    node = xml("<element minValue='10'/>")
    assert parse_min_value(node) == 10
    assert parse_min_value(xml("<element/>")) is None
    with raises(SchemaParsingError):
        parse_min_value(xml("<element minValue='invalid'/>"))
        
def test_parse_null_value():
    node = xml("<element nullValue='0'/>")
    assert parse_null_value(node) == 0
    assert parse_null_value(xml("<element/>")) is None
    with raises(SchemaParsingError):
        parse_null_value(xml("<element nullValue='invalid'/>"))
        
def test_parse_value_ref():
    node = xml("<element valueRef='someValue'/>")
    assert parse_value_ref(node) == "someValue"
    assert parse_value_ref(xml("<element/>")) is None


def test_parse_primitive_type():
    assert parse_primitive_type(xml("<element primitiveType='int'/>")).name == "int"
    assert parse_primitive_type(xml("<element primitiveType='float'/>")).name == "float"
    with raises(SchemaParsingError):
        parse_primitive_type(xml("<element primitiveType='invalid'/>"))
    with raises(SchemaParsingError):
        parse_primitive_type(xml("<element/>"))
        
        
def test_parse_type():
    node = xml("<element type='int'/>")
    assert parse_type(node) == "int"
    with raises(SchemaParsingError):
        parse_type(xml("<element/>"))
        
        
def test_parse_length():
    node = xml("<element length='10'/>")
    assert parse_length(node) == 10
    assert parse_length(xml("<element/>")) == 1
    with raises(SchemaParsingError):
        parse_length(xml("<element length='invalid'/>"))
        
        
def test_parse_semantic_version():
    node = xml("<element semanticVersion='1.0.0'/>")
    assert parse_semantic_version(node) == "1.0.0"
    assert parse_semantic_version(xml("<element/>")) == ""
    
    
def test_parse_byte_order():
    assert parse_byte_order(xml("<element byteOrder='littleEndian'/>")) == ByteOrder.LITTLE_ENDIAN
    assert parse_byte_order(xml("<element byteOrder='bigEndian'/>")) == ByteOrder.BIG_ENDIAN
    assert parse_byte_order(xml("<element/>")) == ByteOrder.LITTLE_ENDIAN
    with raises(SchemaParsingError):
        parse_byte_order(xml("<element byteOrder='invalid'/>"))
        
        
def test_parse_header_type():
    assert parse_header_type(xml('<element headerType="someHeader"/>')) == "someHeader"
    assert parse_header_type(xml('<element/>')) == "messageHeader"
    with raises(SchemaParsingError):
        parse_header_type(xml('<element headerType=""/>'))
        
        
def test_parse_package():
    node = xml("<element package='com.example'/>")
    assert parse_package(node) == "com.example"
    with raises(SchemaParsingError):
        parse_package(xml("<element/>"))
        
        
def test_parse_version():
    node = xml("<element version='1'/>")
    assert parse_version(node) == 1
    with raises(SchemaParsingError):
        parse_version(xml("<element/>"))
    with raises(SchemaParsingError):
        parse_version(xml("<element version='invalid'/>"))
        
        
def test_parse_dimension_type():
    ctx = ParsingContext()
    assert parse_dimension_type(xml("<element dimensionType='decimal'/>"), ctx) == builtin.decimal
    with raises(SchemaParsingError):
        parse_dimension_type(xml("<element dimensionType='int'/>"), ctx)
    with raises(SchemaParsingError):
        parse_dimension_type(xml("<element dimensionType='invalid'/>"), ctx)