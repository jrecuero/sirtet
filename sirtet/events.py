from typing import NewType, List, Tuple, Any


Event = NewType("Event", int)
Result_Event = NewType("Result_Event", List[Tuple[Event, Any]])


class Events:

    NULL = Event(0)
    MOVE_DOWN = Event(1)
    MOVE_LEFT = Event(2)
    MOVE_RIGHT = Event(3)
    ROTATE_CLOCK = Event(4)
    ROTATE_ANTICLOCK = Event(5)
    GAME_OVER = Event(6)
    NEW_PIECE = Event(7)
    MATCH_ROW = Event(8)
    RENDER = Event(9)
    BOTTOMED_PIECE = Event(10)
    EXIT = Event(11)
    MATCH_DAMAGE = Event(12)
