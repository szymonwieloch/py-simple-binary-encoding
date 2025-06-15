from ..schema import (
    ValidValue,
    Enum,
    Type,
    Composite,
    Presence,
    Set,
    Choice,
    FixedLengthElement,
    Ref,
    Message,
    MessageSchema,
    Group,
    Data,
    Field,
)
from lxml.etree import Element
from .attributes import (
    parse_name,
    parse_description,
    parse_since_version,
    parse_deprecated,
    parse_encoding_type,
    parse_offset,
    parse_type as parse_type_attr,
    parse_presence,
    parse_primitive_type,
    parse_length,
    parse_id,
    parse_package,
    parse_version,
    parse_semantic_version,
    parse_byte_order,
    parse_header_type,
    parse_alignment,
    parse_semantic_type,
    parse_block_length,
    parse_dimension_type,
)
from .errors import SchemaParsingError
from .ctx import ParsingContext
from lxml.etree import XMLParser, parse
from lxml import ElementInclude


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

    return ValidValue(
        name=name,
        description=description,
        value=value,
        since_version=since_version,
        deprecated=deprecated,
    )


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

    return Enum(
        name=name,
        description=description,
        since_version=since_version,
        deprecated=deprecated,
        valid_values=valid_values,
        encoding_type=encoding_type,
        offset=offset,
    )


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
        raise SchemaParsingError(
            f"Invalid value for choice '{name}': {node.text}"
        ) from e

    return Choice(
        name=name,
        description=description,
        since_version=since_version,
        deprecated=deprecated,
        value=value,
    )


def parse_set(node: Element) -> Set:
    """Parses a set element from XML.
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

    return Set(
        name=name,
        description=description,
        since_version=since_version,
        deprecated=deprecated,
        offset=offset,
        encoding_type=encoding_type,
        choices=choices,
    )


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
    primitive_type = parse_primitive_type(node)
    offset = parse_offset(node)
    length = parse_length(node)

    presence = parse_presence(node)

    return Type(
        name=name,
        description=description,
        since_version=since_version,
        deprecated=deprecated,
        primitive_type=primitive_type,
        offset=offset,
        presence=presence,
        length=length,
    )


def parse_ref(node: Element, ctx: ParsingContext) -> Ref:
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

    return Ref(
        name=name, description=description, type_=ctx.types[type_], offset=offset
    )


def parse_composite_element(node: Element, ctx: ParsingContext) -> FixedLengthElement:
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
            return parse_ref(node, ctx)
        case "composite":
            return parse_composite(node, ctx)

    raise SchemaParsingError(f"Unknown composite element type: {node.tag}")


def parse_composite(node: Element, ctx: ParsingContext) -> Composite:
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
    offset = parse_offset(node)

    elements = [parse_composite_element(child, ctx) for child in node]

    return Composite(
        name=name,
        description=description,
        since_version=since_version,
        deprecated=deprecated,
        offset=offset,
        elements=elements,
    )


def parse_message_schema(node: Element) -> MessageSchema:
    """Parses a messageSchema element from XML.
    Args:
        node (Element): The XML element representing a message schema.
    Returns:
        MessageSchema: An instance of MessageSchema with parsed attributes.
    """
    if node.tag != "messageSchema":
        raise SchemaParsingError(f"Expected 'messageSchema' tag, got '{node.tag}'")

    package = parse_package(node)
    version = parse_version(node)
    semantic_version = parse_semantic_version(node)
    id_ = parse_id(node)
    byte_order = parse_byte_order(node)
    header_type = parse_header_type(node)

    return MessageSchema(
        package=package,
        version=version,
        semantic_version=semantic_version,
        id=id_,
        byte_order=byte_order,
        header_type=header_type,
    )


def parse_message(node: Element, ctx: ParsingContext) -> Message:
    """
    Parses a message element from XML.

    Args:
        node (Element): The XML element representing a message.

    Returns:
        Message: An instance of Message with parsed attributes.
    """
    if node.tag != "message":
        raise SchemaParsingError(f"Expected 'message' tag, got '{node.tag}'")

    id_ = parse_id(node)
    name = parse_name(node)
    description = parse_description(node)
    semantic_type = parse_semantic_type(node)
    block_length = parse_block_length(node)
    since_version = parse_since_version(node)
    deprecated = parse_deprecated(node)
    alignment = parse_alignment(node)
    
    fields, groups, datas = parse_elements(node, ctx)
    
    return Message(
        id=id_,
        name=name,
        description=description,
        semantic_type=semantic_type,
        block_length=block_length,
        since_version=since_version,
        deprecated=deprecated,
        alignment=alignment,
        fields=fields,
        groups=groups,
        datas=datas,
    )
    
    
def parse_field(node: Element, ctx: ParsingContext) -> Field:
    """
    Parses a field element from XML.

    Args:
        node (Element): The XML element representing a field.

    Returns:
        Field: An instance of Field with parsed attributes.
    """
    if node.tag != "field":
        raise SchemaParsingError(f"Expected 'field' tag, got '{node.tag}'")

    id_ = parse_id(node)
    name = parse_name(node)
    description = parse_description(node)
    type_ = parse_type_attr(node)
    presence = parse_presence(node)
    offset = parse_offset(node)
    since_version = parse_since_version(node)
    deprecated = parse_deprecated(node)
    alignment = parse_alignment(node)
    
    # TODO: value_ref and constant_value parsing
    
    return Field(
        id=id_,
        name=name,
        description=description,
        type=ctx.types[type_],
        presence=presence,
        offset=offset,
        since_version=since_version,
        deprecated=deprecated,
        alignment=alignment,
        value_ref=None,
        constant_value=None,
    )
    
    
def parse_group(node: Element, ctx: ParsingContext) -> Group:
    """
    Parses a group element from XML.

    Args:
        node (Element): The XML element representing a group.

    Returns:
        Group: An instance of Group with parsed attributes.
    """
    if node.tag != "group":
        raise SchemaParsingError(f"Expected 'group' tag, got '{node.tag}'")

    id_ = parse_id(node)
    name = parse_name(node)
    description = parse_description(node)
    block_length = parse_block_length(node)
    since_version = parse_since_version(node)
    deprecated = parse_deprecated(node)
    dimension_type = parse_dimension_type(node, ctx)

    fields, groups, datas = parse_elements(node, ctx)

    return Group(
        id=id_,
        name=name,
        description=description,
        block_length=block_length,
        since_version=since_version,
        deprecated=deprecated,
        fields=fields,
        groups=groups,
        datas=datas,
        dimension_type=dimension_type
    )
    
    
def parse_data(node: Element, ctx: ParsingContext) -> Data:
    """
    Parses a data element from XML.

    Args:
        node (Element): The XML element representing a data element.

    Returns:
        Data: An instance of Data with parsed attributes.
    """
    if node.tag != "data":
        raise SchemaParsingError(f"Expected 'data' tag, got '{node.tag}'")

    name = parse_name(node)
    description = parse_description(node)
    id_ = parse_id(node)
    type_ = parse_type_attr(node)
    semantic_type = parse_semantic_type(node)
    since_version = parse_since_version(node)
    deprecated = parse_deprecated(node)

    return Data(
        name=name,
        id=id_,
        type_=ctx.types[type_],
        description=description,
        semantic_type=semantic_type,
        since_version=since_version,
        deprecated=deprecated,
    )
    
    
def parse_elements(node: Element, ctx: ParsingContext) -> tuple[list[Field], list[Group], list[Data]]:
    """
    Parses a list of elements from XML. This functionality is shared between group and message parsing.

    Args:
        node (Element): The XML element containing child elements to parse.
        ctx (ParsingContext): The parsing context containing type definitions.

    Returns:
        tuple[list[Field], list[Group], list[Data]]: A tuple containing lists of parsed fields, groups, and data elements.
    """
    fields = []
    groups = []
    datas = []

    for child in node:
        match child.tag:
            case "field":
                if datas or groups:
                    raise SchemaParsingError(
                        "Field cannot be defined after data or group elements."
                    )
                fields.append(parse_field(child, ctx))
            case "group":
                if datas:
                    raise SchemaParsingError(
                        "Group cannot be defined after data elements."
                    )
                groups.append(parse_group(child, ctx))
            case "data":
                datas.append(parse_data(child, ctx))
            case _:
                raise SchemaParsingError(f"Unknown element type: {child.tag}")

    return fields, groups, datas


def parse_schema(path) -> MessageSchema:
    """Parses te SBE 2.0 schema file"""
    with open (path, 'rb') as file:
        parser = XMLParser(remote_comments=True)
        root = parser(file, parser=parser).getroot()
        ElementInclude.include(root)