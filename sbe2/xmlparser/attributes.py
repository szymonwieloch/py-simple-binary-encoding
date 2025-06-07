from lxml.etree import Element
from.errors import SchemaParsingError
from ..schema import Presence, ByteOrder

def parse_name(element: Element) -> str:
    """
    Parses the 'name' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        str: The value of the 'name' attribute.
    """
    name = element.get('name', '')
    if not name:
        raise SchemaParsingError(f"Element {element.tag}is missing 'name' attribute")
    return name

def parse_description(element: Element) -> str:
    """
    Parses the 'description' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        str: The value of the 'description' attribute, or an empty string if not present.
    """
    return element.get('description', '').strip()

def parse_since_version(element: Element) -> int:
    """
    Parses the 'sinceVersion' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int: The value of the 'sinceVersion' attribute, or 0 if not present.
    """
    return int(element.get('sinceVersion', '0'))

def parse_deprecated(element: Element) -> int | None:
    """
    Parses the 'deprecated' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int | None: The value of the 'deprecated' attribute, or None if not present.
    """
    deprecated = element.get('deprecated')
    return int(deprecated) if deprecated else None

def parse_offset(element: Element) -> int | None:
    """
    Parses the 'offset' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int | None: The value of the 'offset' attribute, or None if not present.
    """
    offset = element.get('offset')
    return int(offset) if offset else None

def parse_presence(element: Element) -> Presence | None:
    """
    Parses the 'presence' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        Presence: The presence value, defaulting to 'required' if not specified.
    """
    presence_str = element.get('presence')
    if not presence_str:
        return None
    try:
        return Presence(presence_str)
    except ValueError as e:
        raise SchemaParsingError(f"Invalid presence value '{presence_str}' in element {element.tag}") from e
    
def parse_id(element: Element) -> int:
    """
    Parses the 'id' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int: The value of the 'id' attribute
    """
    id_str = element.get('id')
    try:
        return int(id_str)
    except (ValueError, TypeError) as e:
        raise SchemaParsingError(f"Invalid id value '{id_str}' in element {element.tag}") from e
    

def parse_semantic_type(element: Element) -> str:
    """
    Parses the 'semanticType' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        str: The value of the 'semanticType' attribute, or an empty string if not present.
    """
    return element.get('semanticType', '')