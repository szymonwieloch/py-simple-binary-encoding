from lxml.etree import Element
from .errors import SchemaParsingError
from ..schema import Presence, ByteOrder, PrimitiveType, Composite, Type
from .ctx import ParsingContext


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

def parse_encoding_type(element: Element) -> Type:
    """
    Parses the 'encodingType' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        Type: The type associated with the 'encodingType' attribute
    """
    encoding_type = element.get("encodingType", '')
    if not encoding_type:
        raise SchemaParsingError(
            f"Element {element.tag} is missing 'encodingType' attribute"
        )
    return encoding_type


def parse_min_value(element: Element) -> int | None:
    """
    Parses the 'minValue' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int | None: The value of the 'minValue' attribute, or None if not present.
    """
    min_value = element.get("minValue")
    try:
        return int(min_value) if min_value else None
    except (ValueError, TypeError) as e:
        raise SchemaParsingError(
            f"Invalid minValue '{min_value}' in element {element.tag}"
        ) from e
        
def parse_max_value(element: Element) -> int | None:
    """
    Parses the 'maxValue' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int | None: The value of the 'maxValue' attribute, or None if not present.
    """
    max_value = element.get("maxValue")
    try:
        return int(max_value) if max_value else None
    except (ValueError, TypeError) as e:
        raise SchemaParsingError(
            f"Invalid maxValue '{max_value}' in element {element.tag}"
        ) from e
        
        
def parse_null_value(element: Element) -> int | None:
    """
    Parses the 'nullValue' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int | None: The value of the 'nullValue' attribute, or None if not present.
    """
    null_value = element.get("nullValue")
    try:
        return int(null_value) if null_value else None
    except (ValueError, TypeError) as e:
        raise SchemaParsingError(
            f"Invalid nullValue '{null_value}' in element {element.tag}"
        ) from e
        
def parse_character_encoding(element: Element) -> str | None:
    """
    Parses the 'characterEncoding' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        str: The value of the 'characterEncoding' attribute, or None if not present.
    """
    character_encoding = element.get("characterEncoding", "")
    return character_encoding if character_encoding else None


def parse_primitive_type(element: Element) -> PrimitiveType:
    """
    Parses the 'primitiveType' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        str: The value of the 'primitiveType' attribute.
    """
    primitive_type = element.get("primitiveType", "")
    if not primitive_type:
        raise SchemaParsingError(
            f"Element {element.tag} is missing 'primitiveType' attribute"
        )
        
    pt = PrimitiveType.by_name.get(primitive_type)
    if pt is None:
        raise SchemaParsingError(
            f"Unknown primitive type '{primitive_type}' in element {element.tag}"
        )
    return pt


def parse_value_ref(element: Element) -> str | None:
    """
    Parses the 'valueRef' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        str | None: The value of the 'valueRef' attribute, or None if not present.
    """
    vr =  element.get("valueRef", "")
    return vr if vr else None


def parse_type(element:Element) -> str:
    """
    Parses the 'type' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        str: The value of the 'type' attribute.
    """
    type_value = element.get("type", "")
    if not type_value:
        raise SchemaParsingError(
            f"Element {element.tag} is missing 'type' attribute"
        )
    return type_value


def parse_length(element: Element) -> int:
    """
    Parses the 'length' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int: The value of the 'length' attribute.
    """
    length_str = element.get("length", "1")
    try:
        return int(length_str)
    except (ValueError, TypeError) as e:
        raise SchemaParsingError(
            f"Invalid length value '{length_str}' in element {element.tag}"
        ) from e
        
def parse_byte_order(element: Element) -> ByteOrder:
    """
    Parses the 'byteOrder' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        ByteOrder: The byte order value, defaulting to 'littleEndian' if not specified.
    """
    byte_order_str = element.get("byteOrder", "littleEndian")
    try:
        return ByteOrder(byte_order_str)
    except ValueError as e:
        raise SchemaParsingError(
            f"Invalid byte order '{byte_order_str}' in element {element.tag}"
        ) from e
        
def parse_version(element: Element) -> int:
    """
    Parses the 'version' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        int: The value of the 'version' attribute.
    """
    version_str = element.get("version")
    try:
        return int(version_str)
    except (ValueError, TypeError) as e:
        raise SchemaParsingError(
            f"Invalid version value '{version_str}' in element {element.tag}"
        ) from e
        
        
def parse_header_type(element: Element) -> str:
    """
    Parses the 'headerType' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        str: The value of the 'headerType' attribute.
    """
    header_type = element.get("headerType", "messageHeader")
    if not header_type:
        raise SchemaParsingError(
            f"Element {element.tag} is missing 'headerType' attribute"
        )
    return header_type

def parse_package(element: Element, required: bool = True) -> str | None:
    """
    Parses the 'package' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.
        required (bool): If set raises an exception on empty value.

    Returns:
        str | None: The value of the 'package' attribute.
    """
    package = element.get("package", "")
    if not package and required:
        raise SchemaParsingError(
            f"Element {element.tag} is missing 'package' attribute"
        )
    return package or None


def parse_semantic_version(element: Element) -> str:
    """
    Parses the 'semanticVersion' attribute from an XML element.

    Args:
        element (Element): The XML element to parse.

    Returns:
        str: The value of the 'semanticVersion' attribute.
    """
    return element.get("semanticVersion", "")
    # TODO: Validate semantic version format if necessary
    # TODO: is empty string valid?
    
    
def parse_dimension_type(node, ctx: ParsingContext) -> Composite:
    """
    Parses the 'dimensionType' attribute from an XML element.

    Args:
        node (Element): The XML element to parse.
        ctx (ParsingContext): The context of parsing.

    Returns:
        str: The value of the 'dimensionType' attribute.
    """
    dimension_type = node.get("dimensionType", "groupSizeEncoding")
    if not dimension_type:
        raise SchemaParsingError(
            f"Element {node.tag} is missing 'dimensionType' attribute"
        )
    # TODO: validate that the composite meets requirements for a dimension type
    return ctx.types[dimension_type]
