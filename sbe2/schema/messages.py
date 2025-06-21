from .message import Message

class Messages:
    """
    Collection of parsed message schemas
    """
    
    def __init__(self):
        self._by_id:dict[int, Message] = {}
        self._by_name:dict[str, Message] = {}
    
    def add(self, msg: Message):
        """
        Adds message to the collection
        """
        if msg.id in self._by_id:
            raise ValueError(f'Message with ID {msg.id} is already defined')
        if msg.name in self._by_name:
            raise ValueError(f"Message with name '{msg.name}' is already defined")
        self._by_id[msg.id] = msg
        self._by_name[msg.name] = msg
        
        
    def __getitem__(self, key: int|str) -> Message:
        """
        Returns Message by ID or name.
        Raises KeyError if not found.
        """
        if isinstance(key, str):
            return self._by_name[key]
        if isinstance(key, int):
            return self._by_id[key]
        key_type = type(key)
        raise KeyError(f"Unrecognized message key type: '{key_type}'")
    
    def __len__(self) -> int:
        """
        Returns the number of messages in the collection.
        """
        return len(self._by_id)
    

    
    def get(self, key: int|str) -> Message | None:
        """
        Returns Message by ID or name
        """
        if isinstance(key, str):
            return self._by_name.get(key)
        if isinstance(key, int):
            return self._by_id.get(key)