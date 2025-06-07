
from lxml.etree import XML as xml
from sbe2.xmlparser.types import parse_valid_value
def test_parse_valid_value():
    node = xml('<validValue name="something" sinceVersion="5" deprecated="8" >5</validValue>')
    vv = parse_valid_value(node)
    assert vv.name == 'something'
    assert vv.value == 5
    assert vv.since_version == 5
    assert vv.deprecated == 8