'''
The below tests try to parse and validate a real schema from the official SBE repository: https://github.com/aeron-io/simple-binary-encoding/tree/master/sbe-samples/src/main/resources
'''

from os import path
from sbe2.xmlparser import parse_schema
import pytest
from sbe2.schema import ByteOrder, Type, primitive_type, Presence, Enum, Set, Composite

def schema_path(file_name) -> str:
    cur_dir = path.dirname(__file__)
    return path.join(cur_dir, 'example_schema', file_name)


@pytest.mark.no_cover
def test_parse_example_schema():
    schema = parse_schema(schema_path('example-schema.xml'))
    
@pytest.mark.no_cover
def test_parse_example_extension_schema():
    schema = parse_schema(schema_path('example-extension-schema.xml'))
    
    
def test_parse_complete_schema():
    schema = parse_schema(schema_path('complete.xml'))
    assert schema.id == 1
    assert schema.package == 'complete'
    assert schema.version == 4
    assert schema.semantic_version == '5.2'
    assert schema.description == 'Schema which tries to use all features of the SBE XML schema language.'
    assert schema.byte_order == ByteOrder.LITTLE_ENDIAN
    assert schema.header_type_name == 'CustomHeader'
    hdr = schema.header_type
    assert hdr.description == 'Custom header type for the complete schema.'
    assert hdr.name == 'CustomHeader'
    assert hdr.since_version == 0
    assert hdr.deprecated is None
    assert len(hdr.elements) == 7
    assert isinstance(hdr.elements[0], Type)
    assert hdr.elements[0].name == 'blockLength'
    assert hdr.elements[0].primitive_type == primitive_type.uint16
    assert isinstance(hdr.elements[1], Type)
    assert hdr.elements[1].name == 'templateId'
    assert hdr.elements[1].primitive_type == primitive_type.uint16
    assert isinstance(hdr.elements[2], Type)
    assert hdr.elements[2].name == 'schemaId'
    assert hdr.elements[2].primitive_type == primitive_type.uint16
    assert isinstance(hdr.elements[3], Type)
    assert hdr.elements[3].name == 'version'
    assert hdr.elements[3].primitive_type == primitive_type.uint16
    assert isinstance(hdr.elements[4], Type)
    assert hdr.elements[4].name == 'numGroups'
    assert hdr.elements[4].primitive_type == primitive_type.uint16
    assert isinstance(hdr.elements[5], Type)
    assert hdr.elements[5].name == 'numVarDataFields'
    assert hdr.elements[5].primitive_type == primitive_type.uint16
    assert isinstance(hdr.elements[6], Type)
    assert hdr.elements[6].name == 'extra'
    assert hdr.elements[6].primitive_type == primitive_type.uint32

    