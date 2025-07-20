from ..schema import MessageSchema, Types, Messages, FixedLengthElement, Type, Set, Enum, Composite, Choice, ValidValue, Ref
from dataclasses import dataclass
from .errors import Error, Diff
from typing import Any



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
    result.extend(compare_types(old.types, new.types, new_version))
    result.extend(compare_messages(old.messages, new.messages, new_version))
    
    return result


def compare_types(old: Types, new: Types, new_version: int | None) -> list[Diff]:
    """
    Compare two type collections for equality.
    
    Args:
        old (Types): The old type collection.
        new (Types): The new type collection.
        result (list[Diff]): The list to append differences to.
        new_version (int | None): The new schema version, if applicable.
    """
    result = []
    # types are generally used by name
    remaining = set(new)
    for old_type in old:
        new_type = new.get(old_type.name)
        if new_type is None:
            result.append(Diff(f"Type {old_type.name} not found in the new schema", Error.TYPE_NOT_FOUND))
            continue
        result.extend(compare_type(old_type, new_type, new_version))
        remaining.discard(new_type)
    for remaining_type in remaining:
        result.extend(check_new_type(remaining_type, new_version))
    return result
    
    

def compare_messages(old: Messages, new: Messages, new_version: int | None) -> list[Diff]:
    """
    Compare two message collections for equality.
    
    Args:
        old (Messages): The old message collection.
        new (Messages): The new message collection.
        result (list[Diff]): The list to append differences to.
        new_version (int | None): The new schema version, if applicable.
    """
    # Placeholder for message comparison logic
    return []



def compare_type(old_type: FixedLengthElement, new_type: FixedLengthElement, new_version: int | None) -> list[Diff]:
    """
    Compare two types for equality.
    
    Args:
        old_type: The old type.
        new_type: The new type.
        result (list[Diff]): The list to append differences to.
        new_version (int | None): The new schema version, if applicable.
    """
    result: list[Diff] = []
    if type(old_type) != type(new_type):
        result.append(Diff(f"{old_type.name} used to be {type(old_type).__name__} but now it's {type(new_type).__name__}", Error.TYPE_MISMATCH))
        return result
    
    if isinstance(old_type, Type):
        return compare_type_type(old_type, new_type, new_version)
    if isinstance(old_type, Set):
        return compare_type_set(old_type, new_type, new_version)
    if isinstance(old_type, Enum):
        return compare_type_enum(old_type, new_type, new_version)
    if isinstance(old_type, Composite):
        return compare_type_composite(old_type, new_type, new_version)


def check_new_type(new_type: FixedLengthElement, new_version: int | None) -> list[Diff]:
    """
    Check if a new type is valid and append to the result if not.
    
    Args:
        new_type: The new type to check.
        result (list[Diff]): The list to append differences to.
        new_version (int | None): The new schema version, if applicable.
    """
    result = []
    if new_version is None:
        result.append(Diff(f"Type {new_type.name} added without a version change", Error.TYPE_ADDED))
    else:
        if new_type.since_version is None:
            result.append(Diff(f"Type {new_type.name} has no since version, but was added in version {new_version}", Error.TYPE_NO_SINCE_VERSION))
        else:
            if new_type.since_version != new_version:
                result.append(Diff(f"Type {new_type.name} has a since version {new_type.since_version}, which does not match the new schema version {new_version}", Error.TYPE_WRONG_SINCE_VERSION))
    return result
                
                
def compare_type_type(old_type: Type, new_type: Type, new_version: int | None) -> list[Diff]:
    """
    Compare two Type instances for equality.
    
    Args:
        old_type (Type): The old type.
        new_type (Type): The new type.
        result (list[Diff]): The list to append differences to.
        new_version (int | None): The new schema version, if applicable.
    """
    result = []
    if old_type.length != new_type.length:
        result.append(Diff(f"Type lengths do not match: {old_type.length} != {new_type.length}", Error.TYPE_LENGTH_MISMATCH))
    if old_type.character_encoding != new_type.character_encoding:
        result.append(Diff(f"Character encodings do not match: {old_type.character_encoding} != {new_type.character_encoding}", Error.TYPE_CHARACTER_ENCODING_MISMATCH))
    if old_type.primitive_type != new_type.primitive_type:
        result.append(Diff(f"Primitive types do not match: {old_type.primitive_type} != {new_type.primitive_type}", Error.TYPE_PRIMITIVE_TYPE_MISMATCH))
    result.extend(check_common(old_type, new_type, new_version))
    if old_type.presence != new_type.presence:
        result.append(Diff(f"Presence does not match: {old_type.presence} != {new_type.presence}", Error.TYPE_PRESENCE_MISMATCH))
    return result
    
    # Further comparisons can be added as needed
    
def compare_type_set(old_type: Set, new_type: Set, new_version: int | None) -> list[Diff]:
    """
    Compare two Set instances for equality.
    
    Args:
        old_type (Set): The old set type.
        new_type (Set): The new set type.
        new_version (int | None): The new schema version, if applicable.
    """
    
    result = []
    if old_type.name != new_type.name:
        result.append(Diff(f"Set names do not match: {old_type.name} != {new_type.name}", Error.TYPE_NAME_MISMATCH))
        result.extend(check_common(old_type, new_type, new_version))
    return result


def compare_type_set_choices(old: list[Choice], new: list[Choice], new_version: int | None) -> list[Diff]:
    result = []
    matched, missing, added = match_by_value(old, new)
            
    for m in missing:
            result.append(Diff(f"Choice with value {m.value} removed from set", Error.CHOICE_REMOVED))
    for o, n in matched:
        result.extend(compare_choice(o, n, new_version))
    for a in added:
        if new_version is None:
            result.append(Diff(f"Valid value {a.name} added to enum {new.name} without a version change", Error.CHOICE_ADDED))
        else:
            if a.since_version is None:
                result.append(Diff(f"Valid value {a.name} has no since version, but was added in version {new_version}", Error.CHOICE_NO_SINCE_VERSION))
            else:
                if a.since_version != new_version:
                    result.append(Diff(f"Valid value {a.name} has a since version {a.since_version}, which does not match the new schema version {new_version}", Error.CHOICE_WRONG_SINCE_VERSION))
    return result
        
    
    
def compare_choice(old: Choice, new: Choice, new_version: int | None) -> list[Diff]:
    result = []
    result.extend(check_common(old, new, new_version))
    return result
  
def match_by_value(old:list, new: list) -> tuple[list[tuple[Any, Any]], list[Any], list[Any]]:
    '''
    Returns:
        matched pairs, missing, added
    '''
    old_values = {o.value for o in old}
    new_values = {n.value for n in new}
    missing_values = old_values - new_values
    added_values = new_values - old_values
    matched = old_values & new_values
    new_by_value = {n.value: n for n in new}
    return [(o, new_by_value[o.value]) for o in old if o.value in matched] , [o for o in old if o.value in missing_values], [n for n in new if n.value in added_values]
    
def compare_type_enum(old: list[ValidValue], new: list[ValidValue], new_version: int | None) -> list[Diff]:
    result = []
    if old.name != new.name:
        result.append(Diff(f"Enum names do not match: {old.name} != {new.name}", Error.ENUM_NAME_MISMATCH))
        result.extend(check_common(old, new, new_version))
        result.extend(compare_type_enum_valid_values(old, new, new_version))
    return result
    
            
def compare_type_enum_valid_values(old: list[ValidValue], new: list[ValidValue], new_version: int | None) -> list[Diff]:
    result = []
    matched, missing, added = match_by_value(old.valid_values, new.valid_values)
    for m in missing:
            result.append(Diff(f"Valid value with value {m.value} removed from enum {old.name}", Error.VALID_VALUE_REMOVED))
    for old_vv, new_vv in matched:
        result.extend(compare_valid_value(old_vv, new_vv, new_version))
    for new_vv in added:
        if new_version is None:
            result.append(Diff(f"Valid value {new_vv.name} added to enum {new.name} without a version change", Error.VALID_VALUE_ADDED))
        else:
            if new_vv.since_version is None:
                result.append(Diff(f"Valid value {new_vv.name} has no since version, but was added in version {new_version}", Error.VALID_VALUE_NO_SINCE_VERSION))
            else:
                if new_vv.since_version != new_version:
                    result.append(Diff(f"Valid value {new_vv.name} has a since version {new_vv.since_version}, which does not match the new schema version {new_version}", Error.VALID_VALUE_WRONG_SINCE_VERSION))
    return result


def compare_valid_value(old:ValidValue, new:ValidValue, new_version: int | None) -> list[Diff]:
    result = []
    result.extend(check_common(old, new, new_version))
    return result

def compare_type_composite(old: Composite, new: Composite, new_version: int | None) -> list[Diff]:
    result = []
    old_elements = {e.name for e in old.elements}
    new_elements = {e.name for e in new.elements}
    added_elements = new_elements - old_elements
    for ae in added_elements:
        result.append(Diff(f"Composite {old.name} element {ae.name} was added", Error.COMPOSITE_ADDED_ELEMENT))
    missing_elements = old_elements - new_elements
    for me in missing_elements:
        result.append(Diff(f"Composite {old.name} element {me.name} is missing", Error.COMPOSITE_MISSING_ELEMENT))
    matched_elements = old_elements & new_elements
    for me in matched_elements:
        result.extend(compare_type(old, new, new_version))
        
    result.extend(check_common(old, new, new_version))


def type_name(type_: FixedLengthElement):
    if isinstance(type_, ValidValue):
        return 'Valid value'
    return type(type_).__name__

def type_uppercase(t: FixedLengthElement) -> str:
    if isinstance(t, Composite): return "COMPOSITE"
    if isinstance(t, Enum): return "ENUM"
    if isinstance(t, Set): return "SET"
    if isinstance(t, Choice): return "CHOICE"
    if isinstance(t, ValidValue): return "VALID_VALUE"
    if isinstance(t, Type): return "TYPE"
    if isinstance(t, Ref): return "REF"
    raise ValueError(f'Unknown type: {type(t).__name__}')
        

def get_err(t: FixedLengthElement, name: str) -> Error:
    return getattr(Error, f'{type_uppercase(t)}_{name}')
    
            
def check_common(old: FixedLengthElement, new: FixedLengthElement, new_version: int|None) -> list[Diff] :
    result = []
    if old.name != new.name:
        result.append(Diff(f"{type_name(old)} {old.name} name does not match: {old.name} != {new.name}", get_err(old, "NAME_MISMATCH")))
    if old.since_version != new.since_version:
        result.append(Diff(f"{type_name(old)} {old.name} since versions do not match: {old.since_version} != {new.since_version}", get_err(old, "SINCE_VERSION_MISMATCH")))
    if old.deprecated != new.deprecated:
        if old.deprecated is not None or new.deprecated != new_version:
            result.append(Diff(f"{type_name(old)} {old.name} deprecated versions do not match: {old.deprecated} != {new.deprecated}", get_err(old, "DEPRECATED_MISMATCH")))
    return result