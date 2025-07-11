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
    builtin
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
    parse_value_ref,
    parse_character_encoding,
    parse_max_value,
    parse_min_value,
    parse_null_value
)
from .errors import SchemaParsingError
from .ctx import ParsingContext
from lxml.etree import XMLParser, parse, QName
from lxml import ElementInclude
from typing import Any


def parse_valid_value(val_val: Element, encoding_type: str) -> ValidValue:
    """
    Parses a validValue element from XML.

    Args:
        val_val (Element): The XML element representing a valid value.
        enum (Enum): The enumeration type this ValidValue is part of.
        encoding_type (Type): The encoding type for this enum.

    Returns:
        ValidValue: An instance of ValidValue with parsed attributes.
    """
    if val_val.tag != "validValue":
        raise SchemaParsingError(f"Expected 'validValue' tag, got '{val_val.tag}'")
    name = parse_name(val_val)
    description = parse_description(val_val)
    value = val_val.text.encode('ascii') if encoding_type == 'char' else int(val_val.text)
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

    valid_values = [parse_valid_value(vv, encoding_type) for vv in node]
    

    # names and values must be unique
    if len(valid_values) != len(set(vv.name for vv in valid_values)):
        raise SchemaParsingError(f"Duplicate valid value names found in enum '{name}'")
    if len(valid_values) != len(set(vv.value for vv in valid_values)):
        raise SchemaParsingError(f"Duplicate valid value values found in enum '{name}'")

    enum =  Enum(
        name=name,
        description=description,
        since_version=since_version,
        deprecated=deprecated,
        valid_values=valid_values,
        encoding_type_name=encoding_type,
        offset=offset,
    )
    for vv in valid_values:
        vv.enum = enum
    return enum


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
        ctx (ParsingContext): The context of parsing.
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
        encoding_type_name=encoding_type,
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
    value_ref = parse_value_ref(node)
    value = node.text
    character_encoding = parse_character_encoding(node)
    null_value = parse_null_value(node)
    max_value = parse_max_value(node)
    min_value = parse_min_value(node)

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
        value_ref=value_ref,
        value= value,
        character_encoding=character_encoding,
        null_value=null_value,
        max_value=max_value,
        min_value=min_value,
    )


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

    return Ref(
        name=name, description=description, type_name=type_, offset=offset
    )


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
        case "composite":
            return parse_composite(node)

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
    offset = parse_offset(node)

    elements = [parse_composite_element(child) for child in node]

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
    
    #TODO: check namespace?
    qname = QName(node.tag)
    if qname.localname != "messageSchema":
        raise SchemaParsingError(f"Expected 'messageSchema' tag, got '{qname.localname}'")

    package = parse_package(node)
    version = parse_version(node)
    semantic_version = parse_semantic_version(node)
    id_ = parse_id(node)
    byte_order = parse_byte_order(node)
    header_type = parse_header_type(node)
    description = parse_description(node)

    return MessageSchema(
        package=package,
        version=version,
        semantic_version=semantic_version,
        id=id_,
        byte_order=byte_order,
        header_type_name=header_type,
        description=description,
    )
    
def get_package(node:Element) -> str | None:
    """
    Gets a <messages> tag package name for the given message.
    """
    curr = node
    while True:
        curr = curr.getparent()
        if curr is None:
            return None
        if curr.tag == 'messages':
            package = parse_package(curr, required=False)
            if package:
                return package
        


def parse_message(node: Element, ctx: ParsingContext, default_package:str) -> Message:
    """
    Parses a message element from XML.

    Args:
        node (Element): The XML element representing a message.

    Returns:
        Message: An instance of Message with parsed attributes.
    """
    #TODO: check namespace?
    qname = QName(node.tag)
    if qname.localname != "message":
        raise SchemaParsingError(f"Expected 'message' tag, got '{qname.localname}'")

    id_ = parse_id(node)
    name = parse_name(node)
    description = parse_description(node)
    semantic_type = parse_semantic_type(node)
    block_length = parse_block_length(node)
    since_version = parse_since_version(node)
    deprecated = parse_deprecated(node)
    alignment = parse_alignment(node)
    package = get_package(node) or default_package
    
    fields, groups, datas = parse_elements(node, ctx)
    
    return Message(
        id=id_,
        name=name,
        description=description,
        package=package,
        semantic_type=semantic_type,
        block_length=block_length,
        since_version=since_version,
        deprecated=deprecated,
        alignment=alignment,
        fields=fields,
        groups=groups,
        datas=datas,
    )
    
def value_ref_to_valid_value(value_ref:str, ctx:ParsingContext) -> ValidValue:
    try:
        enum_name, valid_value = value_ref.split('.')
        enum = ctx.types[enum_name]
        if not isinstance(enum, Enum):
            raise ValueError(f"'{enum_name}' type is not enum")
        for vv in enum.valid_values:
            if vv.name == valid_value:
                return vv
        raise ValueError(f"Enum '{enum_name}' does not contain value '{valid_value}'")
    except Exception as e:
        raise SchemaParsingError(f"Invalid value reference: '{value_ref}'") from e
    
def field_constant_value(value_ref: str, text: str, type_: FixedLengthElement, ctx: ParsingContext) -> Any:
    value_ref = value_ref or (type_.value_ref if isinstance(type_, Type) else None)
    const_val = text or (type_.const_val if isinstance(type_, Type) else None)
    if bool(value_ref) == bool(const_val):
        raise SchemaParsingError(f"Exactly one of `valueRef' attribute or constant value needs to be defined for the '{node}' field")
    if value_ref:
        return value_ref_to_valid_value(value_ref, ctx).value
    else:
        return type_.parse(const_val)
    
    
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
    type_ = ctx.types[parse_type_attr(node)]
    presence = parse_presence(node)
    offset = parse_offset(node)
    since_version = parse_since_version(node)
    deprecated = parse_deprecated(node)
    alignment = parse_alignment(node)
    value_ref = parse_value_ref(node)
    text = node.text
    const_val = field_constant_value(value_ref, text, type_, ctx) if presence is Presence.CONSTANT else None
    
    return Field(
        id=id_,
        name=name,
        description=description,
        type=type_,
        presence=presence,
        offset=offset,
        since_version=since_version,
        deprecated=deprecated,
        alignment=alignment,
        value_ref=value_ref,
        constant_value=const_val,
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


def parse_type_node(node:Element) -> FixedLengthElement:
    match node.tag:
        case 'type':
            return parse_type(node)
        case 'enum':
            return parse_enum(node)
        case 'set':
            return parse_set(node)
        case 'composite':
            return parse_composite(node)

def parse_schema_fd(fd) -> MessageSchema:
    """
    Parses an SBE schema from a file descriptor.
    Args:
        fd (file-like object): File descriptor containing the XML data.
    Returns:
        MessageSchema: An instance of MessageSchema with parsed attributes.
    Raises:
        SchemaParsingError: If the schema cannot be parsed.
    """
    parser = XMLParser(remove_comments=True)
    root = parse(fd, parser=parser).getroot()
    ElementInclude.include(root)
    schema = parse_message_schema(root)
    
    ctx = ParsingContext(types=schema.types)
    
    for types in root.iter('types'):
        for type_ in types:
            type_def = parse_type_node(type_)
            ctx.types.add(type_def)
    
    for type_def in ctx.types:
        type_def.lazy_bind(ctx.types)
        
    schema.header_type = schema.types.get_composite(schema.header_type_name)
    
    for msg in root.iterfind('.//sbe:message', namespaces=root.nsmap):
        m = parse_message(msg, ctx, schema.package)
        schema.messages.add(m)

    return schema

def parse_schema(path=None, fd=None, text=None) -> MessageSchema:
    """
    Parses an SBE schema from an XML file or string.
    Args:
        path (str, optional): Path to the XML file containing the schema.
        fd (file-like object, optional): File-like object containing the XML data.
        text (str, optional): String containing the XML data.
    Returns:
        MessageSchema: An instance of MessageSchema with parsed attributes.
    Raises:
        SchemaParsingError: If the schema cannot be parsed.
    """
    args = sum(1 for arg in (path, fd, text) if arg is not None)
    if args != 1:
        raise ValueError("Exactly one of 'path', 'fd', or 'text' must be provided")
    
    if path is not None:
        with open (path, 'rb') as file:
            return parse_schema_fd(file)
    elif fd is not None:
        return parse_schema_fd(fd)
    elif text is not None:
        from io import StringIO
        return parse_schema_fd(StringIO(text))