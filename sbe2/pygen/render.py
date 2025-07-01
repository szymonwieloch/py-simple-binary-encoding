from .templates import enum as enum_template, set_ as set_template
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