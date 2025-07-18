from lxml.etree import XML as xml
from sbe2.xmlparser.types import parse_valid_value, parse_enum, parse_choice, parse_set, parse_ref, parse_composite, parse_type, parse_message_schema, parse_message, parse_field, parse_data, parse_group, parse_schema
from sbe2.xmlparser.errors import SchemaParsingError
from sbe2.xmlparser.ctx import ParsingContext
from pytest import raises
from sbe2.schema import Type, Enum, Choice, Set, Ref, ValidValue, Composite, Presence, MessageSchema, ByteOrder, primitive_type
from sbe2.schema import builtin
from unittest.mock import MagicMock


INVALID_NODE = xml(
    """
    <invalid />
    """
)

example_enum = Enum(name="Example", description='', encoding_type_name='int', valid_values=[
        ValidValue(name="Something", description='', value=5),
        ValidValue(name="Nothing", description='', value=7),
    ])



def test_parse_valid_value():
    with raises(SchemaParsingError):
        parse_valid_value(INVALID_NODE, 'int')
        
    node = xml(
        '<validValue name="something" sinceVersion="5" deprecated="8" description="blah" >5</validValue>'
    )
    vv = parse_valid_value(node, 'int')
    assert vv.name == "something"
    assert vv.value == 5
    assert vv.since_version == 5
    assert vv.deprecated == 8
    assert vv.description == "blah"


def test_parse_enum():
    with raises(SchemaParsingError):
        parse_enum(INVALID_NODE)
    
    node = xml(
        """
    <enum name="TestEnum" sinceVersion="1" deprecated="2" description="Test Enum" encodingType="int" offset="0">
        <validValue name="Value1">1</validValue>
        <validValue name="Value2">2</validValue>
    </enum>
    """
    )
    enum = parse_enum(node)
    assert enum.name == "TestEnum"
    assert enum.since_version == 1
    assert enum.deprecated == 2
    assert enum.description == "Test Enum"
    assert enum.encoding_type_name == 'int'
    assert enum.offset == 0
    assert len(enum.valid_values) == 2
    assert enum.valid_values[0].name == "Value1"
    assert enum.valid_values[0].value == 1
    assert enum.valid_values[1].name == "Value2"
    assert enum.valid_values[1].value == 2

    # duplicate names and values should raise an error
    with raises(SchemaParsingError):
        node = xml(
            """
        <enum name="TestEnum" sinceVersion="1" deprecated="2" description="Test Enum" encodingType="int" offset="0">
            <validValue name="Value1">2</validValue>
            <validValue name="Value2">2</validValue>
        </enum>
        """
        )
        parse_enum(node)

    with raises(SchemaParsingError):
        node = xml(
            """
        <enum name="TestEnum" sinceVersion="1" deprecated="2" description="Test Enum" encodingType="int" offset="0">
            <validValue name="Value1">1</validValue>
            <validValue name="Value1">2</validValue>
        </enum>
        """
        )
        parse_enum(node)


def test_parse_choice():
    with raises(SchemaParsingError):
        parse_choice(INVALID_NODE)
        
    node = xml(
        """
    <choice name="TestChoice" sinceVersion="1" deprecated="2" description="Test Choice">6</choice>
    """
    )
    choice = parse_choice(node)
    assert choice.name == "TestChoice"
    assert choice.since_version == 1
    assert choice.deprecated == 2
    assert choice.description == "Test Choice"
    assert choice.value == 6

    with raises(SchemaParsingError):
        node = xml(
            """
        <choice name="TestChoice" sinceVersion="1" deprecated="2" description="Test Choice">invalid</choice>
        """
        )
        parse_choice(node)


def test_parse_set():
    with raises(SchemaParsingError):
        parse_set(INVALID_NODE)

    node = xml(
        """
    <set name="TestSet" sinceVersion="1" deprecated="2" description="Test Set" encodingType="int" offset="0">
        <choice name="Value1">1</choice>
        <choice name="Value2">2</choice>
    </set>
    """
    )
    set_ = parse_set(node)
    assert set_.name == "TestSet"
    assert set_.since_version == 1
    assert set_.deprecated == 2
    assert set_.description == "Test Set"
    assert set_.encoding_type_name == 'int'
    assert set_.offset == 0
    assert len(set_.choices) == 2
    assert set_.choices[0].name == "Value1"
    assert set_.choices[0].value == 1
    assert set_.choices[1].name == "Value2"
    assert set_.choices[1].value == 2

    # duplicate names and values should raise an error

    with raises(SchemaParsingError):
        node = xml(
            """
        <set name="TestSet" sinceVersion="1" deprecated="2" description="Test Set" encodingType="int" offset="0">
            <choice name="Value1">2</choice>
            <choice name="Value2">2</choice>
        </set>
        """
        )
        parse_set(node)
    with raises(SchemaParsingError):
        node = xml(
            """
        <set name="TestSet" sinceVersion="1" deprecated="2" description="Test Set" encodingType="int" offset="0">
            <choice name="Value1">1</choice>
            <choice name="Value1">2</choice>
        </set>
        """
        )
        parse_set(node)


def test_parse_ref():
    with raises(SchemaParsingError):
        parse_ref(INVALID_NODE)

    node = xml(
        """
    <ref name="TestRef" description="Test Reference" type="int" offset="56"/>
    """
    )
    ref = parse_ref(node)
    assert ref.name == "TestRef"
    assert ref.description == "Test Reference"
    assert ref.type_name == 'int'
    assert ref.offset == 56

    with raises(SchemaParsingError):
        node = xml(
            """
        <ref name="TestRef" sinceVersion="1" deprecated="2" description="Test Reference"/>
        """
        )
        parse_ref(node)  # type should be mandatory
        
        
def test_parse_composite():
    with raises(SchemaParsingError):
        parse_composite(INVALID_NODE)

    node = xml(
        """
    <composite name="TestComposite" sinceVersion="1" deprecated="2" description="Test Composite" offset="0">
        <type name="Field1" primitiveType="int" offset="0"/>
        <set name="Field2" encodingType="int" offset="4">
            <choice name="Choice1">1</choice>
            <choice name="Choice2">2</choice>
        </set>
        <enum name="Field3" encodingType="int" offset="8">
            <validValue name="Value1">1</validValue>
            <validValue name="Value2">2</validValue>
        </enum>
        <ref name="Field4" description="Reference Field" type="decimal" offset="12"/>
        <composite name="NestedComposite" sinceVersion="1" deprecated="2" description="Nested Composite">
            <type name="NestedField" primitiveType="float" offset="0"/>
        </composite>
    </composite>
    """
    )
    composite = parse_composite(node)
    assert composite.name == "TestComposite"
    assert composite.since_version == 1
    assert composite.deprecated == 2
    assert composite.description == "Test Composite"
    assert composite.offset == 0
    assert len(composite.elements) == 5
    assert type(composite.elements[0]) == Type
    assert composite.elements[0].name == "Field1"
    assert composite.elements[0].primitive_type is primitive_type.int_
    assert composite.elements[0].offset == 0
    assert type(composite.elements[1]) == Set
    assert composite.elements[1].name == "Field2"
    assert composite.elements[1].encoding_type_name == 'int'
    assert composite.elements[1].offset == 4
    assert len(composite.elements[1].choices) == 2
    assert composite.elements[1].choices[0].name == "Choice1"
    assert composite.elements[1].choices[0].value == 1
    assert composite.elements[1].choices[1].name == "Choice2"
    assert composite.elements[1].choices[1].value == 2
    assert composite.elements[2].name == "Field3"
    assert type(composite.elements[2]) == Enum
    assert composite.elements[2].encoding_type_name == 'int'
    assert composite.elements[2].offset == 8
    assert len(composite.elements[2].valid_values) == 2
    assert composite.elements[2].valid_values[0].name == "Value1"
    assert composite.elements[2].valid_values[0].value == 1
    assert composite.elements[2].valid_values[1].name == "Value2"
    assert composite.elements[2].valid_values[1].value == 2
    assert type(composite.elements[3]) == Ref
    assert composite.elements[3].name == "Field4"
    assert composite.elements[3].description == "Reference Field"
    assert composite.elements[3].type_name == 'decimal'
    assert composite.elements[3].offset == 12
    assert type(composite.elements[4]) == Composite
    assert composite.elements[4].name == "NestedComposite"
    assert composite.elements[4].since_version == 1
    assert composite.elements[4].deprecated == 2
    assert composite.elements[4].description == "Nested Composite"
    assert len(composite.elements[4].elements) == 1
    assert type(composite.elements[4].elements[0]) == Type
    assert composite.elements[4].elements[0].name == "NestedField"
    assert composite.elements[4].elements[0].primitive_type is primitive_type.float_
    assert composite.elements[4].elements[0].offset == 0
    

def test_parse_type():
    with raises(SchemaParsingError):
        parse_type(INVALID_NODE)
    
    node = xml(
        """
    <type name="TestType" primitiveType="int" sinceVersion="1" deprecated="2" description="Test Type" offset="0" presence="required" length="3" characterEncoding="utf-8"/>
    """
    )
    type_ = parse_type(node)
    assert type_.name == "TestType"
    assert type_.primitive_type is primitive_type.int_
    assert type_.since_version == 1
    assert type_.deprecated == 2
    assert type_.description == "Test Type"
    assert type_.offset == 0
    assert type_.presence == Presence.REQUIRED
    assert type_.length == 3
    assert type_.const_val is None
    assert type_.value_ref is None
    assert type_.total_length == 4
    
    
    with raises(SchemaParsingError):
        node = xml(
            """
        <type name="TestType" sinceVersion="1" deprecated="2" description="Test Type"/>
        """
        )
        parse_type(node)  # primitiveType should be mandatory
        
    node = xml(
        """    
        <type name="TestType" primitiveType="int" presence="optional" nullValue="5" maxValue="10" minValue="1"/>
        """)
    type_ = parse_type(node)
    assert type_.name == "TestType"
    assert type_.primitive_type is primitive_type.int_
    assert type_.presence == Presence.OPTIONAL
    assert type_.null_value == 5
    assert type_.max_value == 10
        

def test_parse_type_const_value():
    node = xml(
        """
    <type name="TestType" primitiveType="int" sinceVersion="1" deprecated="2" description="Test Type" offset="0" presence="constant">5</type>
    """
    )
    type_ = parse_type(node)
    assert type_.presence == Presence.CONSTANT
    assert type_.value == '5'
    assert type_.const_val is None
    assert type_.value_ref is None
    
    ctx = ParsingContext()
    type_.lazy_bind(ctx.types)
    assert type_.const_val == 5
    
    
def test_parse_type_value_ref():
    with raises(SchemaParsingError):
        parse_type(INVALID_NODE)
        
    node = xml(
        """
    <type name="TestType" primitiveType="int" sinceVersion="1" deprecated="2" description="Test Type" offset="0" presence="constant" valueRef="Example.Something"/>
    """
    )
    type_ = parse_type(node)
    assert type_.presence == Presence.CONSTANT
    assert type_.value is None
    assert type_.const_val is None
    assert type_.value_ref == "Example.Something"
    
    ctx = ParsingContext()
    ctx.types.add(example_enum)
    type_.lazy_bind(ctx.types)
    assert type_.const_val == 5
    
        
        
def test_parse_message_schema():
    with raises(SchemaParsingError):
        parse_message_schema(INVALID_NODE)
    
    node = xml(
        """
    <messageSchema version="1" package="test.package" headerType="myHeader" byteOrder="bigEndian" id="123" semanticVersion="1.0.0">
    </messageSchema>
    """
    )
    ms = parse_message_schema(node)
    assert ms.version == 1
    assert ms.package == "test.package"
    assert ms.header_type_name == "myHeader"
    assert ms.byte_order == ByteOrder.BIG_ENDIAN
    assert ms.id == 123
    assert ms.semantic_version == "1.0.0"
    
    
def test_parse_message_attributes():
    node = xml(
        """
    <message id="1" name="TestMessage" description="This is a test message" semanticType="test" blockLength="8" sinceVersion="1" deprecated="2" alignment="4">
    </message>
    """
    )
    ctx = ParsingContext()
    message = parse_message(node, ctx, 'package')
    assert message.id == 1
    assert message.name == "TestMessage"
    assert message.description == "This is a test message"
    assert message.semantic_type == "test"
    assert message.block_length == 8
    assert message.since_version == 1
    assert message.deprecated == 2
    assert message.alignment == 4
    assert message.fields == []
    assert message.groups == []
    assert message.datas == []
    assert message.package == 'package'
    
   
def test_parse_message_elements():
    node = xml(
        """
    <message id="1" name="TestMessage">
        <field id="2" name="Field1" type="int"/>
        <group id="3" name="SubGroup" dimensionType="decimal"/>
        <data id="4" name="Data1" type="int"/>
    </message>
    """
    )
    ctx = ParsingContext()
    message = parse_message(node, ctx, 'package')
    assert len(message.fields) == 1
    assert message.fields[0].id == 2
    assert message.fields[0].name == "Field1"
    assert message.fields[0].type == builtin.int_
    assert len(message.groups) == 1
    assert message.groups[0].id == 3
    assert message.groups[0].name == "SubGroup"
    assert message.groups[0].dimension_type == builtin.decimal
    assert len(message.datas) == 1
    assert message.datas[0].id == 4
    assert message.datas[0].name == "Data1"
    assert message.datas[0].type_ == builtin.int_
    assert message.package == 'package'
    
def test_parse_field():
    with raises(SchemaParsingError):
        parse_field(INVALID_NODE, ParsingContext())
        
    node = xml(
        """
    <field id="1" name="TestField" description="This is a test field" type="int" offset="0" alignment="4" presence="required" sinceVersion="1" deprecated="2" />
    """
    )
    ctx = ParsingContext()
    field = parse_field(node, ctx)
    assert field.id == 1
    assert field.name == "TestField"
    assert field.description == "This is a test field"
    assert field.type == builtin.int_
    assert field.offset == 0
    assert field.alignment == 4
    assert field.presence == Presence.REQUIRED
    assert field.since_version == 1
    assert field.deprecated == 2
    assert field.value_ref is None
    assert field.constant_value is None
    
    
def test_parse_field_with_value_ref():
    node = xml(
        """
    <field id="1" name="TestField" type="int" presence="constant" valueRef="Example.Something"/>
    """
    )
    ctx = ParsingContext()
    ctx.types.add(example_enum)
    field = parse_field(node, ctx)
    assert field.id == 1
    assert field.name == "TestField"
    assert field.type == builtin.int_
    assert field.presence == Presence.CONSTANT
    assert field.value_ref == "Example.Something"
    assert field.constant_value == 5
    
def test_parse_field_with_constant_value():
    node = xml(
        """
    <field id="1" name="TestField" type="int" presence="constant">10</field>
    """
    )
    ctx = ParsingContext()
    field = parse_field(node, ctx)
    assert field.id == 1
    assert field.name == "TestField"
    assert field.type == builtin.int_
    assert field.presence == Presence.CONSTANT
    assert field.value_ref is None
    assert field.constant_value == 10
    
    
def test_parse_data():
    with raises(SchemaParsingError):
        parse_data(INVALID_NODE, ParsingContext())
        
    node = xml(
        """
    <data id="123" name="TestData" description="This is a test data" type="int" semanticType="text" sinceVersion="1" deprecated="2" />
    """
    )
    ctx = ParsingContext()
    data = parse_data(node, ctx)
    assert data.id == 123
    assert data.name == "TestData"
    assert data.description == "This is a test data"
    assert data.type_ == builtin.int_
    assert data.semantic_type == "text"
    assert data.since_version == 1
    assert data.deprecated == 2
    
    
def test_parse_group_attributes():
    with raises(SchemaParsingError):
        parse_group(INVALID_NODE, ParsingContext())    

    node = xml(
        """
    <group name="TestGroup" id="1" description="This is a test group" semanticType="test" blockLength="8" sinceVersion="1" deprecated="2" dimensionType="decimal">
    </group>
    """
    )
    ctx = ParsingContext()
    group = parse_group(node, ctx)
    assert group.name == "TestGroup"
    assert group.id == 1
    assert group.description == "This is a test group"
    assert group.block_length == 8
    assert len(group.fields) == 0
    assert len(group.groups) == 0
    assert len(group.datas) == 0
    assert group.dimension_type == builtin.decimal
    assert group.since_version == 1
    assert group.deprecated == 2
    
def test_parse_group_elements():
    node = xml(
        """
    <group name="TestGroup" id="1" dimensionType="decimal">
        <field id="2" name="Field1" type="int"/>
        <group id="3" name="SubGroup" dimensionType="decimal"/>
        <data id="4" name="Data1" type="int"/>
    </group>
    """
    )
    ctx = ParsingContext()
    group = parse_group(node, ctx)
    assert len(group.fields) == 1
    assert group.fields[0].id == 2
    assert group.fields[0].name == "Field1"
    assert group.fields[0].type == builtin.int_
    assert len(group.groups) == 1
    assert group.groups[0].id == 3
    assert group.groups[0].name == "SubGroup"
    assert group.groups[0].dimension_type == builtin.decimal
    assert len(group.datas) == 1
    assert group.datas[0].id == 4
    assert group.datas[0].name == "Data1"
    assert group.datas[0].type_ == builtin.int_
    
    
def test_parse_schema_empty():
    node ="""
        <sbe:messageSchema xmlns:sbe="http://fixprotocol.io/2016/sbe"
                   xmlns:xi="http://www.w3.org/2001/XInclude"
                   package="baseline"
                   id="1"
                   version="0"
                   semanticVersion="5.2"
                   description="Example base schema which can be extended."
                   byteOrder="littleEndian">
            <types>
                <composite name="messageHeader" description="Template ID and length of message root">
                    <type name="blockLength" primitiveType="uint16"/>
                    <type name="templateId" primitiveType="uint16"/>
                    <type name="schemaId" primitiveType="uint16"/>
                    <type name="version" primitiveType="uint16"/>
                    <type name="numGroups" primitiveType="uint16" />
                    <type name="numVarDataFields" primitiveType="uint16" />
                </composite>
            </types>
            <messages package="somepackage">
            </messages>
        </sbe:messageSchema>
    """
    from io import StringIO
    schema = parse_schema(text=node)
    assert schema.version == 0
    assert schema.semantic_version == "5.2"
    assert schema.id == 1
    assert schema.description == "Example base schema which can be extended."
    assert schema.byte_order == ByteOrder.LITTLE_ENDIAN
    assert schema.package == "baseline"
    assert schema.types['messageHeader'] is not None
    assert len(schema.messages) == 0
    
    schema2 = parse_schema(fd=StringIO(node))
   