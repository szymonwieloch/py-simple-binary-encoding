from .templates import enum as enum_template, set_ as set_template, composite as composite_template, header as header_template
from ..schema import Enum, Set, Type, Composite, FixedLengthElement, TypeKind, Ref, Types, ByteOrder, MessageSchema, Messages, Message, Field, Group, Data
from dataclasses import dataclass
import datetime

def render_enum(e: Enum) -> str:
    """
    Render an Enum to a string using the enum template.
    
    Args:
        e (Enum): The Enum object to render.
        
    Returns:
        str: The rendered Enum as a string.
    """
    return enum_template.render(name=e.name, valid_values=e.valid_values, description=repr(e.description) if e.description else None)


def render_set(s: Set) -> str:
    """
    Render a Set to a string using the set template.
    
    Args:
        s (Set): The Set object to render.
        
    Returns:
        str: The rendered Set as a string.
    """
    choices = [{"name": ch.name, 'description': ch.description, 'value': 2**ch.value} for ch in s.choices]
    return set_template.render(name=s.name, choices=choices, description= (s.description or None))

def base_type_name(type_: FixedLengthElement) -> str:
    """
    Get the base type name for a FixedLengthElement.
    
    Args:
        type_ (FixedLengthElement): The FixedLengthElement to get the base type name for.
        
    Returns:
        str: The base type name.
    """
    if isinstance(type_, Enum):
        return type_.name
    if isinstance(type_, Set):
        return type_.name
    if isinstance(type_, Type):
        if type_.length == 1:
            return type_.primitive_type.base_type.__name__
        if type_.character_encoding:
            return 'str'
        if type_.primitive_type.is_byte:
            return 'bytes'
        return 'list[int]'
    if isinstance(type_, Composite):
        return type_.name
    if isinstance(type_, Ref):
        return base_type_name(type_.type_)
    raise TypeError(f"Unsupported type: {type(type_)}")


@dataclass
class CompositeElement:
    name: str
    type_name: str
    description: str = ''
    default_value: str | None = None

def render_composite(c: Composite) -> str:
    """
    Render a Composite to a string.
    
    Args:
        c (Composite): The Composite object to render.
        
    Returns:
        str: The rendered Composite as a string.
    """
    elements: list[CompositeElement] = []
    for element in c.elements:
        elements.append(CompositeElement(
            name=element.name,
            type_name=base_type_name(element),
            description=repr(element.description) if element.description else '',
            default_value=None
        ))
    
    return composite_template.render(name=c.name, elements=elements, description=repr(c.description) if c.description else None)


def render_types(types: Types) -> str:
    """
    Render a collection of types to a string.
    
    Args:
        types (Types): The Types object to render.
        
    Returns:
        str: The rendered types as a string.
    """
    rendered_types = []
    for type_ in types:
        if isinstance(type_, Enum):
            rendered_types.append(render_enum(type_))
            continue
        elif isinstance(type_, Set):
            rendered_types.append(render_set(type_))
            continue
        elif isinstance(type_, Composite):
            rendered_types.append(render_composite(type_))
            continue
        elif isinstance(type_, Type):
            continue  # Types are not rendered directly, they are used in composites or other structures
        raise ValueError(f"Unsupported type kind: {type(type_)}")
    
    return '\n\n'.join(rendered_types)

def render_header(description: str, version:int, semantic_version: str, byte_order: ByteOrder, now:datetime.datetime, schema_file: str|None) -> str:
    """
    Render the header for the generated Python module.
    
    Args:
        description (str): The description of the module.
        version (int): The version of the schema.
        semantic_version (str): The semantic version of the schema.
        
    Returns:
        str: The rendered header as a string.
    """
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    bo = 'big' if byte_order == ByteOrder.BIG_ENDIAN else 'little'
    return header_template.render(description=description, version=version, semantic_version=semantic_version, byte_order=bo, timestamp=ts, schema_file=schema_file)


def render_message(message: MessageSchema) -> str:
    """
    Render a single message to a string.
    
    Args:
        message (MessageSchema): The MessageSchema object to render.
        
    Returns:
        str: The rendered message as a string.
    """
    
    return f"# TODO: message {message.name} with ID {message.id} not implemented yet\n" 



def render_messages(messages: Messages) -> str:
    """
    Render a collection of messages to a string.
    
    Args:
        messages (Messages): The Messages object to render.
        
    Returns:
        str: The rendered messages as a string.
    """
    rendered_messages = []
    for message in messages:
        rendered_messages.append(render_message(message))
    
    return '\n\n'.join(rendered_messages)

def render_schema(schema: MessageSchema) -> str:
    """
    Render the entire schema to a string.
    
    Args:
        schema (MessageSchema): The schema to render.
        
    Returns:
        str: The rendered schema as a string.
    """
    # TODO: add schema file handling
    header = render_header(schema.description, schema.version, schema.semantic_version, schema.byte_order, datetime.datetime.now(), schema_file=None)
    types = render_types(schema.types)
    messages = render_messages(schema.messages)
    
    return f"{header}\n\n{types}\n\n{messages}"