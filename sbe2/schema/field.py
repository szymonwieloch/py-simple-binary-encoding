from .common import FixedLengthElement, Presence

class Field(FixedLengthElement):
    """
    Represents a field in the SBE schema.
    """
    
    id: int
    type: FixedLengthElement
    offset: int | None = None
    alignment: int | None = None
    presence: Presence = Presence.REQUIRED
    value_ref = None
    constant_value = None
    since_version: int = 0
    deprecated: int|None = None