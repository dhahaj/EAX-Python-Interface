from enum import Enum

class State(Enum):
    """The state of the application."""

    IDLE                : int = 0
    PROGRAMMING         : int = 1
    TESTING             : int = 2
    WAITING_FOR_BUTTON  : int = 3
    BLOCKED             : int = 4
    CONNECTING          : int = 5
    CONNECTED           : int = 6
    DISCONNECTED        : int = 7
    UPDATING            : int = 8
    WAITING_FOR_INPUT   : int = 9

    def __str__(self) -> str:
        return f'{self.name}'
    
    def __repr__(self) -> str:
        return f'{self.name}'
    
    def __int__(self) -> int:
        return self.value
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        return self.value == other.value
    
    def __ne__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        return self.value != other.value
    
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        return self.value < other.value
    
    def __le__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        return self.value <= other.value
    
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        return self.value > other.value
    
    def __ge__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        return self.value >= other.value
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    def __bool__(self) -> bool:
        return bool(self.value)
    
    def __index__(self) -> int:
        return self.value
    
    def __or__(self, other: object) -> int:
        if not isinstance(other, State):
            return NotImplemented
        return self.value | other.value
    
    def __ror__(self, other: object) -> int:
        if not isinstance(other, State):
            return NotImplemented
        return other.value | self.value
    
    def __and__(self, other: object) -> int:
        if not isinstance(other, State):
            return NotImplemented
        return self.value & other.value
    
    def __rand__(self, other: object) -> int:
        if not isinstance(other, State):
            return NotImplemented
        return other.value & self.value
    
    def __xor__(self, other: object) -> int:
        if not isinstance(other, State):
            return NotImplemented
        return self.value ^ other.value
    
    def __rxor__(self, other: object) -> int:
        if not isinstance(other, State):
            return NotImplemented
        return other.value ^ self.value
    
    def __invert__(self) -> int:
        return ~self.value
    
    def __add__(self, other: object) -> int:
        if not isinstance(other, State):
            return NotImplemented
        return self.value + other.value
    
    def __radd__(self, other: object) -> int:
        if not isinstance(other, State):
            return NotImplemented
        return other.value + self.value
    
    def __sub__(self, other: object) -> int:
        if not isinstance(other, State):
            return NotImplemented
        return self.value - other.value
    
    def __rsub__(self, other: object) -> int:
        if not isinstance(other, State):
            return NotImplemented
        return other.value - self.value
    
    def __mul__(self, other: object) -> int:
        if not isinstance(other, State):
            return NotImplemented
        return self.value * other.value
    
    