from typing import NewType, Any
from sirtet.point import Point
from sirtet.board import Board
from sirtet.board import Board
from sirtet.shapes import Generator
from sirtet.events import Event, Events
from sirtet.board_handler import BoardHandler, Result_Event
from sirtet.logics.roller.segment import Segment
from sirtet.logics.roller.logic import LogicRoller
from tools.cursor import Cursor


class RollerHandler:
    def __init__(self):
        self.bh: BoardHandler = BoardHandler()
        self.logic: Logic = LogicRoller()

    def setup(self, board: Board, gen: Generator, start_point: Point) -> None:
        self.bh.setup(board, gen, start_point)

    def start(self) -> None:
        self.bh.new_piece_at()

    def render(self) -> None:
        Cursor.print(Cursor.clear_entire_screen())
        Cursor.print(Cursor.move_upper_left(0))
        print()
        print(self.bh.board_to_render())

    def event_handler(self, event: Event, data: Any = None) -> None:
        result: Result_Event = Result_Event([])
        if event == Events.MOVE_DOWN:
            result = self.bh.event_handler(Events.MOVE_DOWN)
        elif event == Events.MOVE_LEFT:
            result = self.bh.event_handler(Events.MOVE_LEFT)
        elif event == Events.MOVE_RIGHT:
            result = self.bh.event_handler(Events.MOVE_RIGHT)
        elif event == Events.ROTATE_ANTICLOCK:
            result = self.bh.event_handler(Events.ROTATE_ANTICLOCK)
        elif event == Events.ROTATE_CLOCK:
            result = self.bh.event_handler(Events.ROTATE_CLOCK)
        else:
            assert False, "Unknown event"
        for event, data in result:
            self.logic.event_handler(event, data)
