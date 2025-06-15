from .common import Element
from dataclasses import dataclass
from .field import Field
from .group import Group
from .data import Data


@dataclass
class Message(Element):
    """
    Represents a message in the SBE schema.
    """
    id: int
    
    fields: list[Field] 
    groups: list[Group] 
    datas: list[Data]
    semantic_type: str = ""
    block_length: int | None = None
    since_version: int = 0
    deprecated: int | None = None
    alignment: int | None = None