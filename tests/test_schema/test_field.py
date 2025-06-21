from sbe2.schema import Field, builtin

def test_field_total_length():
    field = Field(
        name="TestField",
        description="",
        id=1,
        type=builtin.int_,
    )
    assert field.total_length == builtin.int_.total_length