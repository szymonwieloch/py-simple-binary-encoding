from dataclasses import dataclass, field
from .types import Types
from .messages import Messages
from .common import ByteOrder

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
    messages: Messages = field(default_factory=Messages)