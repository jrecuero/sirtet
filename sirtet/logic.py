from typing import NewType, List, Any, NoReturn
from sirtet.cell import Cell
from sirtet.piece import Piece


Logic_Event = NewType("Logic_Event", int)


class Logic:

    GAME_OVER = Logic_Event(1)
    NEW_PIECE = Logic_Event(2)
    MATCH_ROW = Logic_Event(3)

    def __init__(self):
        pass

    def _process_game_over(self) -> NoReturn:
        assert False, "Not implemented"

    def _process_new_piece(self, piece: Piece) -> None:
        assert False, "Not implemented"

    def _process_match_row(self, row: List[List[Cell]]) -> None:
        assert False, "Not implemented"

    def event_handler(self, event: Logic_Event, data: Any):
        if event == Logic.GAME_OVER:
            self._process_game_over()
        elif event == Logic.NEW_PIECE:
            self._process_new_piece(data)
        elif event == Logic.MATCH_ROW:
            self._process_match_row(data)
        else:
            pass
