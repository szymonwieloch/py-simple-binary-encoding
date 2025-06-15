from .common import Element
from dataclasses import dataclass
from .field import Field
from .data import Data

@dataclass
class Group(Element):
    id: int
    fields: list[Field]
    groups: list["Group"]
    datas: list[Data]
    block_length: int | None = None
    