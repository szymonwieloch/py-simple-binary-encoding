# Python Simple Binary Encoding Library

Simple Binary Encoding is an ultra fast binary encoding protocol use commonly in high-frequency trading.
While code generators from schema are publicly available, the protocol lacks Python support and basic tooling.
This project aims to solve those issues.

## Submodules

- `schema` - Python object model of a parsed schema file.
- `xmlparser` - parses a schema file into a Python object model.
- `linter` - (**TODO**) - analyses the schema looking for common mistakes.
- `backcheck` - (**TODO**) - check if the given change applied to the schema is backward compatible, This check added to CI solves the most common issue of breaking the protocol on the binary level while extending it.
- `pygen` - (**TODO**) generates Python code for parsing and encoding messages.
- `pyruntime` - (**TODO**) since Python is a dynamic language, it is possible to generate types in the runtime. This skips the common code-generation part characteristic to all strongly typed languages.

This module can also be used to create support for non-standard programming languages or for creating a non-standard input format (as the standard XML format is one of common complains).

## Example

python3```
from sbe2.xmlparser import parse_schema
schema = parse_schema('schema.xml')
```
