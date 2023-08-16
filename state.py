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