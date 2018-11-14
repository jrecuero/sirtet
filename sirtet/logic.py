from typing import NewType, List, Any
from sirtet.cell import Cell


Logic_Event = NewType("Logic_Event", int)


class Logic:

    NEW_PIECE = Logic_Event(1)
    MATCH_ROW = Logic_Event(2)

    def __init__(self):
        pass

    def process_row(self, row: List[List[Cell]]) -> None:
        for r in row:
            for c in r:
                print(c._content)
        exit(0)

    def event_handler(self, event: Logic_Event, data: Any):
        if event == Logic.NEW_PIECE:
            pass
        elif event == Logic.MATCH_ROW:
            self.process_row(data)
        else:
            pass
