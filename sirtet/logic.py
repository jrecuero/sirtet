from typing import NewType, List, Any, NoReturn
from sirtet.cell import Cell
from sirtet.piece import Piece
from sirtet.events import Event, Events


class Logic:
    def __init__(self):
        pass

    def _process_game_over(self) -> NoReturn:
        assert False, "Not implemented"

    def _process_new_piece(self, piece: Piece) -> None:
        assert False, "Not implemented"

    def _process_bottomed_piece(self, piece: Piece) -> None:
        assert False, "Not implemented"

    def _process_match_row(self, row: List[List[Cell]]) -> None:
        assert False, "Not implemented"

    def _process_render(self) -> None:
        pass

    def event_handler(self, event: Event, data: Any):
        if event == Events.GAME_OVER:
            self._process_game_over()
        elif event == Events.NEW_PIECE:
            self._process_new_piece(data)
        elif event == Events.MATCH_ROW:
            self._process_match_row(data)
        elif event == Events.RENDER:
            self._process_render()
        elif event == Events.BOTTOMED_PIECE:
            self._process_bottomed_piece(data)
        else:
            pass
