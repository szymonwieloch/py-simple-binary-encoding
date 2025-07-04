from .primitive_type import (
    PrimitiveType,
    char as pchar,
    int8 as pint8,
    int_ as pint,
    int16 as pint16,
    int32 as pint32,
    int64 as pint64,
    uint8 as puint8,
    uint16 as puint16,
    uint32 as puint32,
    uint64 as puint64,
    float_ as pfloat,
    double as pdouble,
)
from .composite import Composite
from .type import Type
from .common import Presence


def primitive_type_to_type(primitive_type: PrimitiveType) -> Type:
    """
    Converts a PrimitiveType to a Type.

    Args:
        primitive_type (PrimitiveType): The primitive type to convert.

    Returns:
        Type: A Type instance representing the primitive type.
    """
    return Type(
        name=primitive_type.name,
        primitive_type=primitive_type,
        presence=Presence.REQUIRED,
        length=1,
        since_version=0,
        deprecated=None,
        description=primitive_type.name,
        offset=None,
    )


char = primitive_type_to_type(pchar)
int_ = primitive_type_to_type(pint)
int8 = primitive_type_to_type(pint8)
int16 = primitive_type_to_type(pint16)
int32 = primitive_type_to_type(pint32)
int64 = primitive_type_to_type(pint64)
uint8 = primitive_type_to_type(puint8)
uint16 = primitive_type_to_type(puint16)
uint32 = primitive_type_to_type(puint32)
uint64 = primitive_type_to_type(puint64)
float_ = primitive_type_to_type(pfloat)
double = primitive_type_to_type(pdouble)


decimal = Composite(
    name="decimal",
    description="",
    elements=[
        Type(
            name="mantissa",
            primitive_type=pint64,
            presence=Presence.REQUIRED,
            description="",
        ),
        Type(
            name="exponent",
            primitive_type=pint8,
            presence=Presence.REQUIRED,
            description="",
        ),
    ],
)

decimal32 = Composite(
    name="decimal32",
    description="",
    elements=[
        Type(
            name="mantissa",
            primitive_type=pint64,
            presence=Presence.REQUIRED,
            description="",
        ),
        Type(
            name="exponent",
            primitive_type=pint8,
            presence=Presence.CONSTANT,
            description="",
            const_val=-2,
        ),
    ],
)

decimal64 = Composite(
    name="decimal64",
    description="",
    elements=[
        Type(
            name="mantissa",
            primitive_type=pint64,
            presence=Presence.REQUIRED,
            description="",
        ),
        Type(
            name="exponent",
            primitive_type=pint8,
            presence=Presence.CONSTANT,
            description="",
            const_val=-2,
        ),
    ],
)

__all__ = (
    'char',
    'int_',
    'int8',
    'int16',
    'int32',
    'int64',
    'uint8',
    'uint16',
    'uint32',
    'uint64',
    'float_',
    'double',
    'decimal',
    'decimal32',
    'decimal64'
)
