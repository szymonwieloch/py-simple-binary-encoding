from .templates import enum as enum_template, set_ as set_template, composite as composite_template
from ..schema import Enum, Set, Type, Composite

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
    return set_template.render(name=s.name, choices=choices, description=repr(s.description) if s.description else None)

def render_composite(c: Composite) -> str:
    """
    Render a Composite to a string.
    
    Args:
        c (Composite): The Composite object to render.
        
    Returns:
        str: The rendered Composite as a string.
    """
    elements = []
    # for element in c.elements:
    #     if element.effective_default_value is not None:
    #         elements.append(f"{element.name}: {Type(element.type).base_type.__name__} = {repr(element.effective_default_value)}")
    #     else:
    #         elements.append(f"{element.name}: {Type(element.type).base_type.__name__}")
    
    return composite_template.render(name=c.name, elements=elements, description=repr(c.description) if c.description else None)