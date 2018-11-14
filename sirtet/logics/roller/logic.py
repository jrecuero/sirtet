from typing import List, NoReturn
from sirtet.logic import Logic
from sirtet.cell import Cell
from sirtet.piece import Piece


class LogicRoller(Logic):
    def __init__(self):
        super(LogicRoller, self).__init__()

    def _process_game_over(self) -> NoReturn:
        print("GAME OVER")
        exit(0)

    def _process_new_piece(self, piece: Piece) -> None:
        print(piece)

    def _process_bottomed_piece(self, piece: Piece) -> None:
        print(piece)

    def _process_match_row(self, rows: List[List[Cell]]) -> None:
        for row in rows:
            for cell in row:
                print(cell.to_string())
        exit(0)

    def _process_render(self) -> None:
        print("render")
