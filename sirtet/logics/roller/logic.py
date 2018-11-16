from typing import List, NoReturn
from sirtet.logic import Logic
from sirtet.cell import Cell
from sirtet.piece import Piece
from sirtet.events import Events, Result_Event


class LogicRoller(Logic):
    def __init__(self):
        super(LogicRoller, self).__init__()

    def _process_game_over(self) -> Result_Event:
        result: Result_Event = Result_Event([])
        print("GAME OVER")
        result.append((Events.EXIT, None))
        return result

    def _process_new_piece(self, piece: Piece) -> Result_Event:
        result: Result_Event = Result_Event([])
        print(piece)
        return result

    def _process_bottomed_piece(self, piece: Piece) -> Result_Event:
        result: Result_Event = Result_Event([])
        print(piece)
        return result

    def _process_match_row(self, rows: List[List[Cell]]) -> Result_Event:
        result: Result_Event = Result_Event([])
        for row in rows:
            spores = [cell._content.__class__.__name__ for cell in row]
            damage = spores.count("Damage")
            life = spores.count("Life")
            skill = spores.count("Skill")
            outch = spores.count("Outch")
            print(spores)
            print(
                "damage: {} life: {} skill: {} outch: {}".format(
                    damage, life, skill, outch
                )
            )
            result.append(
                (
                    Events.MATCH_DAMAGE,
                    {"damage": damage, "life": life, "skill": skill, "outch": outch},
                )
            )
        return result

    def _process_render(self) -> Result_Event:
        result: Result_Event = Result_Event([])
        print("render")
        return result
