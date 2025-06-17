'''
The below tests try to parse and validate a real schema from the official SBE repository: https://github.com/aeron-io/simple-binary-encoding/tree/master/sbe-samples/src/main/resources
'''

from os import path
from sbe2.xmlparser import parse_schema

def schema_path(file_name) -> str:
    cur_dir = path.dirname(__file__)
    return path.join(cur_dir, 'example_schema', file_name)

def test_parse_example_schema():
    schema = parse_schema(schema_path('example-schema.xml'))