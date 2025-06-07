import enum

class Presence(enum.StrEnum):
    'Matches the `presence` attribute in the schema.'
    REQUIRED = "required"
    OPTIONAL = "optional"
    CONSTANT = "constant"

class ByteOrder(enum.StrEnum):
    'Matches the `byteOrder` attribute in the schema.'
    BIG_ENDIAN = "bigEndian"
    LITTLE_ENDIAN = "littleEndian"

