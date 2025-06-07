from ..schema import ValidValue
from lxml.etree import Element
from .attributes import parse_name, parse_description, parse_since_version, parse_deprecated

def parse_valid_value(val_val: Element) -> ValidValue:
    """
    Parses a validValue element from XML.

    Args:
        val_val (Element): The XML element representing a valid value.

    Returns:
        ValidValue: An instance of ValidValue with parsed attributes.
    """
    name = parse_name(val_val)
    descr = parse_description(val_val)
    value = int(val_val.text)
    since_version = parse_since_version(val_val)
    deprecated = parse_deprecated(val_val)

    return ValidValue(name=name, description=descr, value=value, since_version=since_version, deprecated=deprecated)