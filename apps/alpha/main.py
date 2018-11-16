import time
import curses
from sirtet.cell import Cell
from sirtet.point import Point
from sirtet.matrix import Mat
from sirtet.board import Board
from sirtet.shapes import Generator
from sirtet.events import Events
from sirtet.assets.cells import Block
from sirtet.logics.roller.segment import Segment
from sirtet.logics.roller.handler import RollerHandler
from sirtet.logics.roller.dummy import Dummy


class BoardText(Board):
    def __init__(self, mat: Mat = None):
        super(BoardText, self).__init__(mat)

    def new_cell_empty(self) -> Cell:
        return Block(0)

    def new_cell_border(self) -> Cell:
        return Block(1)


def main(stdscr):
    # Make stdscr.getch non-blocking
    stdscr.nodelay(True)

    h = RollerHandler()
    h.setup(BoardText(), Generator(Segment), Point(0, 1))
    h.player = Dummy("ME", 100, 1, 100)
    h.enemies.append(Dummy("ORC", 50, 1, 10))
    h.start()
    counter = 0
    while True:
        stdscr.clear()
        h.render(stdscr)
        # key = input("Enter: ").lower()
        key = stdscr.getch()
        # Clear out anything else the user has typed in
        curses.flushinp()

        if key == ord("x"):
            exit(0)
        elif key == ord("d"):
            h.event_handler(Events.MOVE_DOWN)
        elif key == ord("a"):
            h.event_handler(Events.MOVE_LEFT)
        elif key == ord("s"):
            h.event_handler(Events.MOVE_RIGHT)
        elif key == ord("q"):
            h.event_handler(Events.ROTATE_ANTICLOCK)
        elif key == ord("w"):
            h.event_handler(Events.ROTATE_CLOCK)
        time.sleep(0.05)
        if counter == 20:
            h.event_handler(Events.MOVE_DOWN)
            counter = 0
        else:
            counter += 1


if __name__ == "__main__":
    curses.wrapper(main)
