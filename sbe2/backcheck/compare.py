from ..schema import MessageSchema, Types, Messages, FixedLengthElement, Type Set, Enum, Composite
from dataclasses import dataclass
from .errors import Error, Diff



def compare(old: MessageSchema, new: MessageSchema) -> list[Diff]:
    """
    Compare two message schemas for equality.
    
    Args:
        old (MessageSchema): The old message schema.
        new (MessageSchema): The new message schema.
        
    Returns:
        list[Diff]: A list of differences found between the two schemas.
    """
    result = []
    if old.id != new.id:
        result.append(Diff(f"Schema IDs do not match: {old.id} != {new.id}", Error.SCHEMA_ID_MISMATCH))
    if old.version != new.version and old.version + 1 != new.version:
        result.append(Diff(f"Schema versions do not match, old: {old.version}, new: {new.version}", Error.SCHEMA_VERSION_MISMATCH))
    if old.package != new.package:
        result.append(Diff(f"Schema packages do not match: {old.package} != {new.package}", Error.SCHEMA_PACKAGE_MISMATCH))
    if old.byte_order != new.byte_order:
        result.append(Diff(f"Byte orders do not match: {old.byte_order.name} != {new.byte_order.name}", Error.SCHEMA_BYTE_ORDER_MISMATCH))
        
    if old.version == new.version:
        if old.semantic_version != new.semantic_version:
            result.append(Diff(f"Semantic versions do not match: {old.semantic_version} != {new.semantic_version}", Error.SCHEMA_SEMANTIC_VERSION_MISMATCH))
    else:
        if old.semantic_version == new.semantic_version:
            result.append(Diff(f"Version has changed, but semantic version is the same: {old.semantic_version}", Error.SCHEMA_SEMANTIC_VERSION_NOT_UPDATED))
            
    new_version = new.version if new.version != old.version else None
    compare_types(old.types, new.types, result, new_version)
    compare_messages(old.messages, new.messages, result, new_version)
    
    return result


def compare_types(old: Types, new: Types, result: list[Diff], new_version: int | None):
    """
    Compare two type collections for equality.
    
    Args:
        old (Types): The old type collection.
        new (Types): The new type collection.
        result (list[Diff]): The list to append differences to.
        new_version (int | None): The new schema version, if applicable.
    """
    # types are generally used by name
    remaining = set(new)
    for old_type in old:
        new_type = new.get(old_type.name)
        if new_type is None:
            result.append(Diff(f"Type {old_type.name} not found in the new schema", Error.TYPE_NOT_FOUND))
            continue
        compare_type(old_type, new_type, result, new_version)
        remaining.discard(new_type)
    for remaining_type in remaining:
        check_new_type(remaining_type, result, new_version)
    
    

def compare_messages(old: Messages, new: Messages, result: list[Diff], new_version: int | None):
    """
    Compare two message collections for equality.
    
    Args:
        old (Messages): The old message collection.
        new (Messages): The new message collection.
        result (list[Diff]): The list to append differences to.
        new_version (int | None): The new schema version, if applicable.
    """
    # Placeholder for message comparison logic
    pass



def compare_type(old_type: FixedLengthElement, new_type: FixedLengthElement, result: list[Diff], new_version: int | None):
    """
    Compare two types for equality.
    
    Args:
        old_type: The old type.
        new_type: The new type.
        result (list[Diff]): The list to append differences to.
        new_version (int | None): The new schema version, if applicable.
    """
    if isinstance(old_type, Type):
        return compare_type_type(old_type, new_type, result, new_version)
    if isinstance(old_type, Set):
        return compare_type_set(old_type, new_type, result, new_version)
    if isinstance(old_type, Enum):
        return compare_type_enum(old_type, new_type, result, new_version)
    if isinstance(old_type, Composite):
        return compare_type_composite(old_type, new_type, result, new_version)


def check_new_type(new_type: FixedLengthElement, result: list[Diff], new_version: int | None):
    """
    Check if a new type is valid and append to the result if not.
    
    Args:
        new_type: The new type to check.
        result (list[Diff]): The list to append differences to.
        new_version (int | None): The new schema version, if applicable.
    """
    if new_version is None:
        result.append(Diff(f"Type {new_type.name} added without a version change", Error.TYPE_ADDED))
    else:
        if new_type.since_version is None:
            result.append(Diff(f"Type {new_type.name} has no since version, but was added in version {new_version}", Error.TYPE_NO_SINCE_VERSION))
        else:
            if new_type.since_version != new_version:
                result.append(Diff(f"Type {new_type.name} has a since version {new_type.since_version}, which does not match the new schema version {new_version}", Error.TYPE_WRONGþ_SINCE_VERSION))
                
                
def compare_type_type(old_type: Type, new_type: Type, result: list[Diff], new_version: int | None):
    """
    Compare two Type instances for equality.
    
    Args:
        old_type (Type): The old type.
        new_type (Type): The new type.
        result (list[Diff]): The list to append differences to.
        new_version (int | None): The new schema version, if applicable.
    """
    if not isinstance(new_type, Type):
        result.append(Diff(f"Expected Type, got {type(new_type).__name__}", Error.TYPE_MISMATCH))
        return
    if old_type.name != new_type.name:
        result.append(Diff(f"Type names do not match: {old_type.name} != {new_type.name}", Error.TYPE_NAME_MISMATCH))
    if old_type.length != new_type.length:
        result.append(Diff(f"Type lengths do not match: {old_type.length} != {new_type.length}", Error.TYPE_LENGTH_MISMATCH))
    if old_type.character_encoding != new_type.character_encoding:
        result.append(Diff(f"Character encodings do not match: {old_type.character_encoding} != {new_type.character_encoding}", Error.TYPE_CHARACTER_ENCODING_MISMATCH))
    if old_type.primitive_type != new_type.primitive_type:
        result.append(Diff(f"Primitive types do not match: {old_type.primitive_type} != {new_type.primitive_type}", Error.TYPE_PRIMITIVE_TYPE_MISMATCH))
    if old_type.since_version != new_type.since_version:
            result.append(Diff(f"Since versions do not match: {old_type.since_version} != {new_type.since_version}", Error.TYPE_SINCE_VERSION_MISMATCH))
    if old_type.deprecated != new_type.deprecated:
        if old_type.deprecated is not None or new_type.deprecated != new_version:
            result.append(Diff(f"Deprecated versions do not match: {old_type.deprecated} != {new_type.deprecated}", Error.TYPE_DEPRECATED_MISMATCH))
    if old_type.presence != new_type.presence:
        result.append(Diff(f"Presence does not match: {old_type.presence} != {new_type.presence}", Error.TYPE_PRESENCE_MISMATCH))
    
    # Further comparisons can be added as needed