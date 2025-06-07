from .common import ByteOrder, Presence
from .enum import Enum, ValidValue
from .type import Type
from .composite import Composite
from lxml.etree import Element 

def parse_valid_value(val_val: Element) -> ValidValue:
    """
    Parses a ValidValue element from XML.
    
    Args:
        val_val (Element): The XML element representing a valid value.
        
    Returns:
        ValidValue: An instance of ValidValue with parsed attributes.
    """
    name = val_val.get('name')
    value = int(val_val.text)
    since_version = int(val_val.get('sinceVersion', 0))
    deprecated = int(val_val.get('deprecated', 0)) if val_val.get('deprecated') else None
    
    return ValidValue(name=name, value=value, since_version=since_version, deprecated=deprecated)