# import time
import curses
from sirtet.cell import Cell
from sirtet.point import Point
from sirtet.matrix import Mat
from sirtet.board import Board
from sirtet.shapes import Generator

from sirtet.events import Events
from sirtet.assets.cells import Block as cBlock
from sirtet.logics.roller.segment import Segment
from sirtet.logics.roller.handler import RollerHandler
from sirtet.logics.roller.dummy import Dummy
from engine.nobject import Caller
from engine.handler import Handler, EVT_ENG_KEY, EVT_ENG_TIMER
from engine.scene import Scene


class BoardText(Board):
    def __init__(self, mat: Mat = None):
        super(BoardText, self).__init__(mat)

    def new_cell_empty(self) -> Cell:
        return cBlock(0)

    def new_cell_border(self) -> Cell:
        return cBlock(1)


class SceneSirtet(Scene):
    def __init__(self):
        super(SceneSirtet, self).__init__("Sirtet")
        self.rh: RollerHandler

    def setup(self):
        self.rh = RollerHandler()
        self.rh.setup(BoardText(), Generator(Segment), Point(0, 4))
        self.rh.player = Dummy("ME", 100, 1, 100, True)
        self.rh.enemies = [Dummy("ORC-{}".format(i), 20, 1, 10) for i in range(2)]
        self.add_object(Caller(0, 0, lambda: "Player: {}\n".format(self.rh.player)))
        self.add_object(
            Caller(5, 0, lambda: "Enemy:  {}\n".format(self.rh.enemies[self.rh.ienemy]))
        )
        self.add_object(Caller(10, 0, self.rh.bhandler.board_to_render_ascii))
        self.rh.start()

    def update(self, *events):
        for event in events:
            if event.evt == EVT_ENG_KEY:
                key = event.get_key()
                if key is not None:
                    if key == ord("x"):
                        exit(0)
                    elif key == ord(" "):
                        self.rh.event_handler(Events.MOVE_DOWN)
                    elif key == ord("k"):
                        self.rh.event_handler(Events.MOVE_LEFT)
                    elif key == ord("l"):
                        self.rh.event_handler(Events.MOVE_RIGHT)
                    elif key == ord("a"):
                        self.rh.event_handler(Events.ROTATE_ANTICLOCK)
                    elif key == ord("s"):
                        self.rh.event_handler(Events.ROTATE_CLOCK)
            elif event.evt == EVT_ENG_TIMER:
                self.rh.event_handler(Events.MOVE_DOWN)


def main(stdscr):
    h = Handler()
    h.add_scene(SceneSirtet())
    h.new_timer(100)
    h.run()


if __name__ == "__main__":
    curses.wrapper(main)
