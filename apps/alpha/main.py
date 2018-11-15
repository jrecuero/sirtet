from sirtet.cell import Cell
from sirtet.point import Point
from sirtet.matrix import Mat
from sirtet.board import Board
from sirtet.shapes import Generator
from sirtet.events import Events
from sirtet.assets.cells import Block
from sirtet.logics.roller.segment import Segment
from sirtet.logics.roller.handler import RollerHandler


class BoardText(Board):
    def __init__(self, mat: Mat = None):
        super(BoardText, self).__init__(mat)

    def new_cell_empty(self) -> Cell:
        return Block(0)

    def new_cell_border(self) -> Cell:
        return Block(1)


if __name__ == "__main__":
    h = RollerHandler()
    h.setup(BoardText(), Generator(Segment), Point(0, 1))
    h.start()
    while True:
        h.render()
        key = input("Enter: ").lower()
        if key == "x":
            exit(0)
        elif key == "":
            h.event_handler(Events.MOVE_DOWN)
        elif key == "a":
            h.event_handler(Events.MOVE_LEFT)
        elif key == "s":
            h.event_handler(Events.MOVE_RIGHT)
        elif key == "q":
            h.event_handler(Events.ROTATE_ANTICLOCK)
        elif key == "w":
            h.event_handler(Events.ROTATE_CLOCK)
