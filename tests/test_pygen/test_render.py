from sbe2.schema import Enum, ValidValue, builtin, Set, Choice, Composite, Ref, Type, primitive_type, Presence
from sbe2.pygen.render import render_enum, render_set, render_composite


def test_render_enum():
    e = Enum(
        name="TestEnum",
        description="This is a test enum",
        valid_values=[
            ValidValue(name="ONE", value=1, description="This is the first value"),
            ValidValue(name="TWO", value=2, description="This is the second value"),
            ValidValue(name="THREE", value=3, description="This is the third value"),
        ],
        encoding_type_name="uint16",
        encoding_type=builtin.uint16,
    )
    rendered = render_enum(e)
    expected = """class TestEnum(enum.Enum):
    'This is a test enum'
    ONE = 1 # This is the first value
    TWO = 2 # This is the second value
    THREE = 3 # This is the third value
"""
    assert rendered == expected
    
    
    
def test_render_set():
    s = Set(
        name="TestSet",
        description="This is a test set",
        choices=[
            Choice(name="BLUE", value=0, description="This is the first choice"),
            Choice(name="RED", value=1, description="This is the second choice"),
            Choice(name="GREEN", value=2, description="This is the third choice"),
        ],
        encoding_type_name="uint8",
        encoding_type=builtin.uint8,
    )
    rendered = render_set(s)
    expected = """class TestSet(enum.Flag):
    'This is a test set'
    BLUE = 1 # This is the first choice
    RED = 2 # This is the second choice
    GREEN = 4 # This is the third choice
"""
    assert rendered == expected
    
    
def test_render_composite():
    c = Composite(
        name="TestComposite",
        description="This is a test composite",
        elements=[
            Ref(name="test_ref", description='', type_name="Something"),
            Type(name="test_type", primitive_type=primitive_type.uint32, description='', presence=Presence.REQUIRED),
            Composite(name="NestedComposite", elements=[], description=''),
            Set(name="test_set", choices=[], encoding_type_name="uint8", encoding_type=builtin.uint8, description=''),
            Enum(name="test_enum", valid_values=[], encoding_type_name="uint8", encoding_type=builtin.uint8, description=''),
        ],
    )
    rendered = render_composite(c)
    expected = """@dataclass
class TestComposite:
    'This is a test composite'
"""
    assert rendered == expected

   