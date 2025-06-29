from .common import FixedLengthElement
from .builtin import decimal, decimal32, decimal64, int16, int32, int64, int8, uint16, uint32, uint64, float_, double, char, int_, uint8
from .type import Type
from .composite import Composite


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
        self.add(int16)
        self.add(int32)
        self.add(int64)
        self.add(int8)
        self.add(uint16)
        self.add(uint32)
        self.add(uint64)
        self.add(float_)
        self.add(double)
        self.add(char)
        self.add(int_)
        self.add(uint8)
        
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
    
    def get(self, name: str) -> FixedLengthElement | None:
        """
        Retrieves a type by its name, returning None if it does not exist.
        
        Args:
            name (str): The name of the type to retrieve.
        
        Returns:
            FixedLengthElement | None: The type with the specified name or None if not found.
        """
        return self._types.get(name)
    
    def __iter__(self):
        return iter(self._types.values())
    
    
    def get_composite(self, name:str):
        com = self[name]
        if not isinstance(com, Composite):
            raise ValueError(f"Type '{name}' is not composite but '{type(com)}'")
        return com
    
    def get_type(self, name:str):
        type_ = self[name]
        if not isinstance(type_, Type):
            raise ValueError(f"Type '{name}' is not type but '{type(type_)}'")
        return type_