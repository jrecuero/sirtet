from typing import List, Any, Dict, cast
from sirtet.point import Point
from sirtet.board import Board
from sirtet.cell import Cell
from sirtet.shapes import Generator
from sirtet.events import Event, Events, Result_Event
from sirtet.piece import Piece
from sirtet.matrix import Mat
from sirtet.board_handler import BoardHandler
from sirtet.logics.roller.dummy import Dummy

# from tools.cursor import Cursor


class RollerHandler:
    def __init__(self):
        self.bhandler: BoardHandler = BoardHandler()
        self.player: Dummy = None
        self.enemies: List[Dummy] = []
        self.ienemy: int = 0

    def setup(self, board: Board, gen: Generator, start_point: Point) -> None:
        self.bhandler.setup(board, gen, start_point)

    def start(self) -> None:
        self.bhandler.new_piece_at()

    def _process_new_piece(self, piece: Piece) -> Result_Event:
        result: Result_Event = Result_Event([])
        # print(piece)
        return result

    def _process_bottomed_piece(self, piece: Piece) -> Result_Event:
        result: Result_Event = Result_Event([])
        # print(piece)
        return result

    def _process_match_row(self, rows: List[List[Cell]]) -> Result_Event:
        result: Result_Event = Result_Event([])
        for row in rows:
            spores = [cell._content.__class__.__name__ for cell in row]
            damage = spores.count("Damage")
            life = spores.count("Life")
            skill = spores.count("Skill")
            outch = spores.count("Outch")
            # print(spores)
            # print(
            #     "damage: {} life: {} skill: {} outch: {}".format(
            #         damage, life, skill, outch
            #     )
            # )
            result.append(
                (
                    Events.MATCH_DAMAGE,
                    {"damage": damage, "life": life, "skill": skill, "outch": outch},
                )
            )
        return result

    def _process_match_damage(self, data: Dict) -> Result_Event:
        result: Result_Event = Result_Event([])
        self.player.healed(self.player.get_life(data["life"]))
        self.player.skilled(self.player.get_skill(data["skill"]))
        self.enemies[self.ienemy].damaged(self.player.get_damage(data["damage"]))
        self.player.damaged(self.enemies[self.ienemy].get_damage(data["outch"]))
        if self.enemies[self.ienemy].life <= 0:
            self.ienemy += 1
            if self.ienemy == len(self.enemies):
                result.append((Events.GAME_OVER, None))
        return result

    def _process_game_over(self) -> Result_Event:
        result: Result_Event = Result_Event([])
        # print("GAME OVER")
        result.append((Events.EXIT, None))
        return result

    def _process_render(self) -> Result_Event:
        result: Result_Event = Result_Event([])
        return result

    def _process_render_ascii(self, screen: Any) -> Result_Event:
        result: Result_Event = Result_Event([])
        screen.addstr(0, 0, "Player: {}\n".format(self.player))
        screen.addstr(5, 0, "Enemy:  {}\n".format(self.enemies[self.ienemy]))
        screen.addstr(10, 0, "{}".format(self.bhandler.board_to_render_ascii()))
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
        elif event == Events.BOTTOMED_PIECE:
            result = self._process_bottomed_piece(cast(Piece, data))
        elif event == Events.NEW_PIECE:
            result = self._process_new_piece(cast(Piece, data))
        elif event == Events.MATCH_ROW:
            result = self._process_match_row(cast(Mat, data))
        elif event == Events.MATCH_DAMAGE:
            result = self._process_match_damage(cast(Dict, data))
        elif event == Events.RENDER:
            result = self._process_render()
        elif event == Events.RENDER_ASCII:
            result = self._process_render_ascii(data)
        elif event == Events.GAME_OVER:
            result = self._process_game_over()
        elif event == Events.EXIT:
            exit(0)
        else:
            assert False, "Unknown event"
        # fallback any events returned by local handlers.
        for event, data in result:
            self.event_handler(event, data)
