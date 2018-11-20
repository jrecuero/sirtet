from typing import List, Any
from sirtet.cell import Cell
from sirtet.piece import Piece
from sirtet.events import Event, Events, Result_Event


class Logic:
    def __init__(self):
        pass

    def _process_game_over(self) -> Result_Event:
        assert False, "Not implemented"

    def _process_new_piece(self, piece: Piece) -> Result_Event:
        assert False, "Not implemented"

    def _process_bottomed_piece(self, piece: Piece) -> Result_Event:
        assert False, "Not implemented"

    def _process_match_row(self, row: List[List[Cell]]) -> Result_Event:
        assert False, "Not implemented"

    def _process_render(self) -> Result_Event:
        assert False, "Not implemented"

    def event_handler(self, event: Event, data: Any) -> Result_Event:
        result: Result_Event = Result_Event([])
        if event == Events.GAME_OVER:
            result = self._process_game_over()
        elif event == Events.NEW_PIECE:
            result = self._process_new_piece(data)
        elif event == Events.MATCH_ROW:
            result = self._process_match_row(data)
        elif event == Events.RENDER:
            result = self._process_render()
        elif event == Events.BOTTOMED_PIECE:
            result = self._process_bottomed_piece(data)
        else:
            pass
        return result
