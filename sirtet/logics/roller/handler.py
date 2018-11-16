from typing import NewType, List, Any, Dict, cast
from sirtet.point import Point
from sirtet.board import Board
from sirtet.shapes import Generator
from sirtet.events import Event, Events, Result_Event
from sirtet.board_handler import BoardHandler
from sirtet.logics.roller.segment import Segment
from sirtet.logics.roller.dummy import Dummy
from sirtet.logics.roller.logic import LogicRoller

# from tools.cursor import Cursor


class RollerHandler:
    def __init__(self):
        self.bhandler: BoardHandler = BoardHandler()
        self.logic: Logic = LogicRoller()
        self.player: Dummy = None
        self.enemies: List[Dummy] = []

    def setup(self, board: Board, gen: Generator, start_point: Point) -> None:
        self.bhandler.setup(board, gen, start_point)

    def start(self) -> None:
        self.bhandler.new_piece_at()

    def render(self, stdscr) -> None:
        # Cursor.print(Cursor.clear_entire_screen())
        # Cursor.print(Cursor.move_upper_left(0))
        # stdscr.addstr("\n")
        stdscr.addstr(0, 0, "Player: {}\n".format(self.player))
        stdscr.addstr(1, 0, "Enemy:  {}\n".format(self.enemies[0]))
        # stdscr.addstr("\n")
        stdscr.addstr(3, 0, "{}".format(self.bhandler.board_to_render()))

    def _process_match_damage(self, data: Dict) -> Result_Event:
        result: Result_Event = Result_Event([])
        self.player.healed(self.player.get_life(data["life"]))
        self.player.skilled(self.player.get_skill(data["skill"]))
        self.enemies[0].damaged(self.player.get_damage(data["damage"]))
        self.player.damaged(self.enemies[0].get_damage(data["outch"]))
        return result

    def event_handler(self, event: Event, data: Any = None) -> None:
        result: Result_Event = Result_Event([])
        if event in [
            Events.MOVE_DOWN,
            Events.MOVE_LEFT,
            Events.MOVE_RIGHT,
            Events.ROTATE_ANTICLOCK,
            Events.ROTATE_CLOCK,
        ]:
            result = self.bhandler.event_handler(event, data)
        elif event in [
            Events.GAME_OVER,
            Events.NEW_PIECE,
            Events.MATCH_ROW,
            Events.RENDER,
            Events.BOTTOMED_PIECE,
        ]:
            result = self.logic.event_handler(event, data)
        elif event == Events.EXIT:
            exit(0)
        elif event == Events.MATCH_DAMAGE:
            result = self._process_match_damage(cast(Dict, data))
        else:
            assert False, "Unknown event"
        # fallback any events returned by local handlers.
        for event, data in result:
            self.event_handler(event, data)
