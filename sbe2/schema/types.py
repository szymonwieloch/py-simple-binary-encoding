from .common import FixedLengthElement
from .builtin import decimal, decimal32, decimal64, primitive_type_to_type, int16, int32, int64, int8, uint16, uint32, uint64, float_, double, char, int_, uint8

class Types:
    """
    This class contains built-in and defined types for the schema.
    It includes primitive types, enums, choices, sets, and composites.
    """
    
    def __init__(self):
        self._types : dict[str: FixedLengthElement] = {}
        self.add(decimal)
        self.add(decimal32)
        self.add(decimal64)
        self.add(primitive_type_to_type(int16))
        self.add(primitive_type_to_type(int32))
        self.add(primitive_type_to_type(int64))
        self.add(primitive_type_to_type(int8))
        self.add(primitive_type_to_type(uint16))
        self.add(primitive_type_to_type(uint32))
        self.add(primitive_type_to_type(uint64))
        self.add(primitive_type_to_type(float_))
        self.add(primitive_type_to_type(double))
        self.add(primitive_type_to_type(char))
        self.add(primitive_type_to_type(int_))
        self.add(primitive_type_to_type(uint8))
        
    def __len__(self):
        """
        Returns the number of types in the collection.
        
        Returns:
            int: The number of types.
        """
        return len(self._types)
        
        
    def add(self, type_: FixedLengthElement):
        """
        Adds a type to the collection.
        
        Args:
            type_ (FixedLengthElement): The type to add.
        """
        if type_.name in self._types:
            raise ValueError(f"Type '{type_.name}' already exists.")
        self._types[type_.name] = type_
        
    def __getitem__(self, name: str) -> FixedLengthElement:
        """
        Retrieves a type by its name.
        Args:
            name (str): The name of the type to retrieve.
        Returns:
            FixedLengthElement: The type with the specified name.
        Raises:
            KeyError: If the type does not exist.
        """
        if name not in self._types:
            raise KeyError(f"Type '{name}' does not exist.")
        return self._types[name]