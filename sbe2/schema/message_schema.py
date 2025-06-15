from dataclasses import dataclass, field
from .types import Types
from .common import ByteOrder
from.message import Message

@dataclass
class MessageSchema:
    """
    Represents the SBE schema.
    """
    package: str
    version: int
    id: int
    semantic_version:str = ""
    header_type: str = "messageHeader"
    byte_order: ByteOrder = ByteOrder.LITTLE_ENDIAN
    types: Types = field(default_factory=Types)
    messages: list[Message] = field(default_factory=list) # TODO: replace it with a dedicated Messages class