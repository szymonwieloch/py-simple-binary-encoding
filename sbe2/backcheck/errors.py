from dataclasses import dataclass
import enum


class Error(enum.Enum):
    """
    Represents the type of error that can occur during schema comparison.
    """

    def __init__(self, id_: str, description: str):
        self.id = id_
        self.description = description

    SCHEMA_ID_MISMATCH = ("schema-id-mismatch", "Schema IDs do not match.")
    SCHEMA_VERSION_MISMATCH = (
        "schema-version-mismatch",
        "Schema versions do not match. Backward compatibility check is only possible if the newer schema either has the same version or a version higher by 1.",
    )
    SCHEMA_PACKAGE_MISMATCH = (
        "schema-package-mismatch",
        "Schema packages do not match.",
    )
    SCHEMA_BYTE_ORDER_MISMATCH = (
        "schema-byte-order-mismatch",
        "Byte orders do not match.",
    )
    SCHEMA_SEMANTIC_VERSION_MISMATCH = (
        "schema-semantic-version-mismatch",
        "Semantic versions do not match.",
    )
    SCHEMA_SEMANTIC_VERSION_NOT_UPDATED = (
        "schema-semantic-version-not-updated",
        "Semantic version has not been updated, but the schema version has been updated.",
    )

    TYPE_REMOVED = ("type-removed", "Type was removed.")
    TYPE_ADDED = (
        "type-added",
        "Type was added to the schema even though the version has not changed.",
    )
    TYPE_NO_SINCE_VERSION = (
        "type-no-since-version",
        "Type has no since version attribute, but it was added to the new schema.",
    )
    TYPE_WRONG_SINCE_VERSION = (
        "type-wrong-since-version",
        "Type has since version attribute, but it is wrong.",
    )
    TYPE_CONVERTED = ("type-converted", "Type was converted to a different type.")
    TYPE_NAME_MISMATCH = ("type-name-mismatch", "Type names do not match.")
    TYPE_LENGTH_MISMATCH = ("type-length-mismatch", "Type lengths do not match.")
    TYPE_CHARACTER_ENCODING_MISMATCH = (
        "type-character-encoding-mismatch",
        "Type character encodings do not match.",
    )
    TYPE_PRIMITIVE_TYPE_MISMATCH = (
        "type-primitive-type-mismatch",
        "Type primitive types do not match.",
    )
    TYPE_SINCE_VERSION_MISMATCH = (
        "type-since-version-mismatch",
        "Type since versions do not match.",
    )
    TYPE_DEPRECATED_MISMATCH = (
        "type-deprecated-mismatch",
        "Type deprecation versions do not match.",
    )
    TYPE_CONST_VALUE_MISMATCH = (
        "type-const-value-mismatch",
        "Type constant values do not match.",
    )
    TYPE_PRESENCE_MISMATCH = ("type-presence-mismatch", "Type presence does not match.")

    CHOICE_ADDED = (
        "choice-added",
        "Set choice was added to the schema even though the version has not changed.",
    )
    CHOICE_REMOVED = ("choice-removed", "Set choice was removed.")
    CHOICE_NO_SINCE_VERSION = (
        "choice-no-since-version",
        "Set choice has no since version attribute, but it was added to the new schema.",
    )
    CHOICE_SINCE_VERSION_MISMATCH = (
        "choice-since-version-mismatch",
        "Set choice since versions do not match.",
    )
    CHOICE_DEPRECATED_MISMATCH = (
        "choice-deprecated-mismatch",
        "Set choice deprecation versions do not match.",
    )
    CHOICE_NAME_MISMATCH = ("choice-name-mismatch", "Set choice names do not match.")


    
    
    
    VALID_VALUE_ADDED = (
        "valid-value-added",
        "Enum valid value was added to the schema even though the version has not changed.",
    )
    VALID_VALUE_REMOVED = ("valid-value-removed", "Enum valid value was removed.")
    VALID_VALUE_NO_SINCE_VERSION = (
        "valid-value-no-since-version",
        "Enum valid value has no since version attribute, but it was added to the new schema.",
    )
    VALID_VALUE_SINCE_VERSION_MISMATCH = (
        "valid-value-since-version-mismatch",
        "Enum valid value since versions do not match.",
    )
    VALID_VALUE_DEPRECATED_MISMATCH = (
        "valid-value-deprecated-mismatch",
        "Enum valid value deprecation versions do not match.",
    )
    VALID_VALUE_NAME_MISMATCH = ("valid-value-name-mismatch", "Enum valid value names do not match.")
    
    COMPOSITE_ADDED_ELEMENT = ('composite-added-element', "An element was added to a composite.")
    COMPOSITE_MISSING_ELEMENT = ('composite-missing-element', "An element was removed from a composite")
    COMPOSITE_SINCE_VERSION_MISMATCH = ('composite-since-version-mismatch', "Composite since versions do not match.")
    COMPOSITE_DEPRECATED_MISMATCH = ("composite-deprecated-mismatch", "Composite deprecation versions do not match.")


@dataclass
class Diff:
    """
    Represents a a difference between two schemas.
    """

    message: str
    error: Error
