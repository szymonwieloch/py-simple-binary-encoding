from lxml.etree import Element
from .errors import SchemaParsingError
from ..schema import Presence, ByteOrder


def parse_name(element: Element) -> str:
    """
    Parses the 'name' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        str: The value of the 'name' attribute.
    """
    name = element.get("name", "")
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
    return element.get("description", "").strip()


def parse_since_version(element: Element) -> int:
    """
    Parses the 'sinceVersion' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int: The value of the 'sinceVersion' attribute, or 0 if not present.
    """
    return int(element.get("sinceVersion", "0"))


def parse_deprecated(element: Element) -> int | None:
    """
    Parses the 'deprecated' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int | None: The value of the 'deprecated' attribute, or None if not present.
    """
    deprecated = element.get("deprecated")
    try:
        return int(deprecated) if deprecated else None
    except (ValueError, TypeError) as e:
        raise SchemaParsingError(
            f"Invalid deprecated value '{deprecated}' in element {element.tag}"
        ) from e


def parse_offset(element: Element) -> int | None:
    """
    Parses the 'offset' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int | None: The value of the 'offset' attribute, or None if not present.
    """
    offset = element.get("offset")
    try:
        return int(offset) if offset else None
    except (ValueError, TypeError) as e:
        raise SchemaParsingError(
            f"Invalid offset value '{offset}' in element {element.tag}"
        ) from e


def parse_presence(element: Element) -> Presence | None:
    """
    Parses the 'presence' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        Presence: The presence value, defaulting to 'required' if not specified.
    """
    presence_str = element.get("presence")
    if not presence_str:
        return None
    try:
        return Presence(presence_str)
    except ValueError as e:
        raise SchemaParsingError(
            f"Invalid presence value '{presence_str}' in element {element.tag}"
        ) from e


def parse_id(element: Element) -> int:
    """
    Parses the 'id' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int: The value of the 'id' attribute
    """
    id_str = element.get("id")
    try:
        return int(id_str)
    except (ValueError, TypeError) as e:
        raise SchemaParsingError(
            f"Invalid id value '{id_str}' in element {element.tag}"
        ) from e


def parse_semantic_type(element: Element) -> str:
    """
    Parses the 'semanticType' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        str: The value of the 'semanticType' attribute, or an empty string if not present.
    """
    return element.get("semanticType", "")


def parse_alignment(element: Element) -> int | None:
    """
    Parses the 'alignment' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int | None: The value of the 'alignment' attribute, or None if not present.
    """
    alignment = element.get("alignment")
    try:
        return int(alignment) if alignment else None
    except (ValueError, TypeError) as e:
        raise SchemaParsingError(
            f"Invalid alignment value '{alignment}' in element {element.tag}"
        ) from e


def parse_block_length(element: Element) -> int | None:
    """
    Parses the 'blockLength' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int | None: The value of the 'blockLength' attribute, or None if not present.
    """
    block_length = element.get("blockLength")
    try:
        return int(block_length) if block_length else None
    except (ValueError, TypeError) as e:
        raise SchemaParsingError(
            f"Invalid blockLength value '{block_length}' in element {element.tag}"
        ) from e

def parse_encoding_type(element: Element) -> str | None:
    """
    Parses the 'encodingType' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        str: The value of the 'encodingType' attribute
    """
    encoding_type = element.get("encodingType", '')
    if not encoding_type:
        raise SchemaParsingError(
            f"Element {element.tag} is missing 'encodingType' attribute"
        )
    return encoding_type