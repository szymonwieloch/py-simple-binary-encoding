from ..schema import ValidValue, Enum, Type, Composite, Presence, Set, Choice, FixedLengthElement, Ref
from lxml.etree import Element
from .attributes import parse_name, parse_description, parse_since_version, parse_deprecated, parse_encoding_type, parse_offset, parse_type as parse_type_attr
from .errors import SchemaParsingError

def parse_valid_value(val_val: Element) -> ValidValue:
    """
    Parses a validValue element from XML.

    Args:
        val_val (Element): The XML element representing a valid value.

    Returns:
        ValidValue: An instance of ValidValue with parsed attributes.
    """
    if val_val.tag != "validValue":
        raise SchemaParsingError(f"Expected 'validValue' tag, got '{val_val.tag}'")
    name = parse_name(val_val)
    description = parse_description(val_val)
    value = int(val_val.text)
    since_version = parse_since_version(val_val)
    deprecated = parse_deprecated(val_val)

    return ValidValue(name=name, description=description, value=value, since_version=since_version, deprecated=deprecated)


def parse_enum(node: Element) -> Enum:
    """
    Parses an enum element from XML.

    Args:
        node (Element): The XML element representing an enum.

    Returns:
        Enum: An instance of Enum with parsed attributes.
    """
    if node.tag != "enum":
        raise SchemaParsingError(f"Expected 'enum' tag, got '{node.tag}'")
    name = parse_name(node)
    description = parse_description(node)
    since_version = parse_since_version(node)
    deprecated = parse_deprecated(node)
    encoding_type = parse_encoding_type(node)
    offset = parse_offset(node)

    valid_values = [parse_valid_value(vv) for vv in node]
    
    # names and values must be unique
    if len(valid_values) != len(set(vv.name for vv in valid_values)):
        raise SchemaParsingError(f"Duplicate valid value names found in enum '{name}'")
    if len(valid_values) != len(set(vv.value for vv in valid_values)):
        raise SchemaParsingError(f"Duplicate valid value values found in enum '{name}'")

    return Enum(name=name, description=description, since_version=since_version, deprecated=deprecated, valid_values=valid_values, encoding_type=encoding_type, offset=offset)


def parse_choice(node: Element) -> Choice:
    """
    Parses a choice element from XML.

    Args:
        node (Element): The XML element representing a choice.

    Returns:
        Choice: An instance of Choice with parsed attributes.
    """
    if node.tag != "choice":
        raise SchemaParsingError(f"Expected 'choice' tag, got '{node.tag}'")
    
    name = parse_name(node)
    description = parse_description(node)
    since_version = parse_since_version(node)
    deprecated = parse_deprecated(node)
    try:
        value = int(node.text)
    except (ValueError, TypeError) as e:
        raise SchemaParsingError(f"Invalid value for choice '{name}': {node.text}") from e
    
    return Choice(name=name, description=description, since_version=since_version, deprecated=deprecated, value=value)

def parse_set(node: Element) -> Set:
    """    Parses a set element from XML.   
    Args:
        node (Element): The XML element representing a set.
    Returns:
        Set: An instance of Set with parsed attributes. 
    """
    if node.tag != "set":
        raise SchemaParsingError(f"Expected 'set' tag, got '{node.tag}'")
    
    name = parse_name(node)
    description = parse_description(node)
    since_version = parse_since_version(node)
    deprecated = parse_deprecated(node)
    encoding_type = parse_encoding_type(node)
    offset = parse_offset(node)
    choices = [parse_choice(choice) for choice in node]
    
    # names and values must be unique
    if len(choices) != len(set(choice.name for choice in choices)):        
        raise SchemaParsingError(f"Duplicate choice names found in set '{name}'")
    if len(choices) != len(set(choice.value for choice in choices)):
        raise SchemaParsingError(f"Duplicate choice value found in set '{name}'")
    
    return Set(name=name, description=description, since_version=since_version, deprecated=deprecated, offset=offset, encoding_type=encoding_type, choices=choices)


def parse_type(node: Element) -> Type:
    """
    Parses a type element from XML.

    Args:
        node (Element): The XML element representing a type.

    Returns:
        Type: An instance of Type with parsed attributes.
    """
    if node.tag != "type":
        raise SchemaParsingError(f"Expected 'type' tag, got '{node.tag}'")
    
    name = parse_name(node)
    description = parse_description(node)
    since_version = parse_since_version(node)
    deprecated = parse_deprecated(node)
    encoding_type = parse_encoding_type(node)
    offset = parse_offset(node)
    
    presence = Presence.from_string(node.get("presence", "optional"))
    
    return Type(name=name, description=description, since_version=since_version, deprecated=deprecated, encoding_type=encoding_type, offset=offset, presence=presence)


def parse_ref(node: Element) -> Ref:
    """
    Parses a ref element from XML.

    Args:
        node (Element): The XML element representing a reference.

    Returns:
        FixedLengthElement: An instance of Ref with parsed attributes.
    """
    if node.tag != "ref":
        raise SchemaParsingError(f"Expected 'ref' tag, got '{node.tag}'")
    
    name = parse_name(node)
    description = parse_description(node)
    type_ = parse_type_attr(node)
    offset = parse_offset(node)
    
    return Ref(name=name, description=description, type_=type_, offset=offset)

def parse_composite_element(node: Element) -> FixedLengthElement:
    """
    Parses a composite element from XML.

    Args:
        node (Element): The XML element representing a composite element.

    Returns:
        FixedLengthElement: An instance of FixedLengthElement with parsed attributes.
    """
    match node.tag:
        case "enum":
            return parse_enum(node)
        case "type":
            return parse_type(node)
        case "set":
            return parse_set(node)
        case "ref":
            return parse_ref(node)
    
    raise SchemaParsingError(f"Unknown composite element type: {node.tag}")

def parse_composite(node: Element) -> Composite:
    """
    Parses a composite element from XML.

    Args:
        node (Element): The XML element representing a composite.

    Returns:
        Composite: An instance of Composite with parsed attributes.
    """
    if node.tag != "composite":
        raise SchemaParsingError(f"Expected 'composite' tag, got '{node.tag}'")
    
    name = parse_name(node)
    description = parse_description(node)
    since_version = parse_since_version(node)
    deprecated = parse_deprecated(node)
    encoding_type = parse_encoding_type(node)
    offset = parse_offset(node)
    
    elements = [parse_composite_element(child) for child in node]
    
    return Composite(name=name, description=description, since_version=since_version, deprecated=deprecated, encoding_type=encoding_type, offset=offset, elements=elements)

