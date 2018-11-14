from typing import NewType, Any
from sirtet.point import Point
from sirtet.board import Board
from sirtet.board import Board
from sirtet.shapes import Generator
from sirtet.board_handler import BoardHandler
from sirtet.logics.roller.segment import Segment
from sirtet.logics.roller.logic import LogicRoller
from tools.cursor import Cursor

HR_Event = NewType("HR_Event", int)


class RollerHandler:

    MOVE_DOWN = HR_Event(1)
    MOVE_LEFT = HR_Event(2)
    MOVE_RIGHT = HR_Event(3)
    ROTATE_CLOCK = HR_Event(4)
    ROTATE_ANTICLOCK = HR_Event(5)

    def __init__(self):
        self.bh: BoardHandler = BoardHandler()
        self.logic: Logic = LogicRoller()

    def setup(self, board: Board, gen: Generator, start_point: Point) -> None:
        board.set_mat(board.new_clean_mat())
        self.bh.setup(board, gen, self.logic, start_point)

    def start(self) -> None:
        self.bh.new_piece_at()

    def render(self) -> None:
        Cursor.print(Cursor.clear_entire_screen())
        Cursor.print(Cursor.move_upper_left(0))
        print()
        print(self.bh.board_to_render())

    def event_handler(self, event: HR_Event, data: Any = None) -> None:
        if event == RollerHandler.MOVE_DOWN:
            self.bh.event_handler(BoardHandler.MOVE_DOWN)
        elif event == RollerHandler.MOVE_LEFT:
            self.bh.event_handler(BoardHandler.MOVE_LEFT)
        elif event == RollerHandler.MOVE_RIGHT:
            self.bh.event_handler(BoardHandler.MOVE_RIGHT)
        elif event == RollerHandler.ROTATE_ANTICLOCK:
            self.bh.event_handler(BoardHandler.ROTATE_ANTICLOCK)
        elif event == RollerHandler.ROTATE_CLOCK:
            self.bh.event_handler(BoardHandler.ROTATE_CLOCK)
        else:
            assert False, "Unknown event"
