from .primitive_type import PrimitiveType
from .composite import Composite
from .type import Type
from.common import Presence

char = PrimitiveType(name='char', length=1, max_value=126, min_value=26, default_null_value=0, base_type=str)
int_ = PrimitiveType(name='int', length=4, max_value=2**31-1, min_value=-(2**31-1), default_null_value=-(2**31), base_type=int)
int8 = PrimitiveType(name='int8', length=1, max_value=127, min_value=-127, default_null_value=-128, base_type=int)
int16 = PrimitiveType(name='int16', length=2, max_value=(2**15-1), min_value=-(2**15-1), default_null_value=-(2**15), base_type=int)
int32 = PrimitiveType(name='int32', length=4, max_value=(2**31-1), min_value=-(2**31-1), default_null_value=-(2**31), base_type=int)
int64 = PrimitiveType(name='int64', length=8, max_value=(2**63-1), min_value=-(2**63-1), default_null_value=-(2**63), base_type=int)
uint8 = PrimitiveType(name='uint8', length=1, max_value=2**8-2, min_value=0, default_null_value=2**8-1, base_type=int)
uint16 = PrimitiveType(name='uint16', length=2, max_value=2**16-2, min_value=0, default_null_value=2**16-1, base_type=int)
uint32 = PrimitiveType(name='uint32', length=4, max_value=2**32-2, min_value=0, default_null_value=2**32-1, base_type=int)
uint64 = PrimitiveType(name='uint64', length=8, max_value=2**64-2, min_value=0, default_null_value=2**64-1, base_type=int)
float_ = PrimitiveType(name='float', length=4, max_value=float('inf'), min_value=-float('inf'), default_null_value=float('nan'), base_type=float)
double = PrimitiveType(name='double', length=8, max_value=float('inf'), min_value=-float('inf'), default_null_value=float('nan'), base_type=float)

decimal = Composite(
    name='decimal',
    description='',
    elements=[
        Type(name='mantissa', primitive_type=int64, presence=Presence.REQUIRED, description=''),
        Type(name='exponent', primitive_type=int8, presence=Presence.REQUIRED, description=''),
    ]
)

decimal32 = Composite(
    name='decimal32',
    description='',
    elements=[
        Type(name='mantissa', primitive_type=int64, presence=Presence.REQUIRED, description=''),
        Type(name='exponent', primitive_type=int8, presence=Presence.CONSTANT, description='', const_val=-2),
    ]
)

decimal64 = Composite(
    name='decimal64',
    description='',
    elements=[
        Type(name='mantissa', primitive_type=int64, presence=Presence.REQUIRED, description=''),
        Type(name='exponent', primitive_type=int8, presence=Presence.CONSTANT, description='', const_val=-2),
    ]
)

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
        offset=None
    )