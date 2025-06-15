from .common import Element
from dataclasses import dataclass
from .field import Field
from .data import Data
from .type import Type
@dataclass
class Group(Element):
    id: int
    fields: list[Field]
    groups: list["Group"]
    datas: list[Data]
    dimension_type: Type
    block_length: int | None = None
    since_version: int = 0
    deprecated: int | None = None
    