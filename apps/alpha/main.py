from sirtet.cell import Cell
from sirtet.point import Point
from sirtet.board import Board
from sirtet.shapes import Generator
from sirtet.board_handler import BoardHandler
from sirtet.assets.cells import Segment, Int
from tools.cursor import Cursor


class BoardText(Board):
    def new_cell_empty(self) -> Cell:
        return Int(0)

    def new_cell_border(self) -> Cell:
        return Int(1)


if __name__ == "__main__":
    bh: BoardHandler = BoardHandler()
    b = BoardText()
    # b.set_mat(self.board.new_clean_mat())
    bh.setup(b, Generator(Segment), Point(0, 1))
    bh.new_piece_at()
    while True:
        Cursor.print(Cursor.clear_entire_screen())
        Cursor.print(Cursor.move_upper_left(0))
        print()
        print(bh.render_to())
        key = input("Enter: ").lower()
        if key == "x":
            exit(0)
        elif key == "":
            bh.event_handler(BoardHandler.MOVE_DOWN)
        elif key == "a":
            bh.event_handler(BoardHandler.MOVE_LEFT)
        elif key == "s":
            bh.event_handler(BoardHandler.MOVE_RIGHT)
        elif key == "q":
            bh.event_handler(BoardHandler.ROTATE_ANTICLOCK)
        elif key == "w":
            bh.event_handler(BoardHandler.ROTATE_CLOCK)
