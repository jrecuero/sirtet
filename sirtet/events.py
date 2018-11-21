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
    NEW_PIECE = Event(10)
    BOTTOMED_PIECE = Event(11)
    MATCH_ROW = Event(12)
    MATCH_DAMAGE = Event(13)
    RENDER = Event(20)
    RENDER_ASCII = Event(21)
    GAME_OVER = Event(100)
    EXIT = Event(101)
