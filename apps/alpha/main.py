from typing import List
from sirtet.cell import Cell
from sirtet.point import Point
from sirtet.matrix import Mat
from sirtet.board import Board
from sirtet.shapes import Generator

from sirtet.events import Events
from sirtet.assets.cells import Block as cBlock
from sirtet.logics.roller.segment import Segment
from sirtet.logics.roller.handler import RollerHandler
from sirtet.logics.roller.jobs import Warrior
from sirtet.logics.roller.dummy import Dummy
from engine.nobject import Caller, BoxText, FlashText, Input, String
from engine.handler import Handler
from engine.event import Event, EVT, KeyHandler, EventNextScene
from engine.scene import Scene, update


class BoardText(Board):
    def __init__(self, mat: Mat = None):
        super(BoardText, self).__init__(mat)

    def new_cell_empty(self) -> Cell:
        return cBlock(0)

    def new_cell_border(self) -> Cell:
        return cBlock(1)


class SceneIntro(Scene):
    def setup(self):
        self.add_object(BoxText(0, 0, "Sirtet"))
        self.add_object(FlashText(5, 0, "press 'c' to continue", self.new_timer(50)))
        self.kh = KeyHandler({"x": lambda: exit(0), "c": lambda: [EventNextScene()]})

    @update
    def update(self, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
            else:
                event_to_return.append(event)
        return event_to_return


class SceneSelect(Scene):
    def setup(self):
        self.enemies_obj = Input(5, 0, "How many enemies? ")
        self.add_object(self.enemies_obj)
        self.timer = None
        self.enemies_nbr: int = 0
        self.kh = KeyHandler({"x": lambda: exit(0)})

    @update
    def update(self, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
            elif event.evt == EVT.ENG.TIMER:
                if event.get_timer() == self.timer:
                    event_to_return.append(EventNextScene())
            elif event.evt == EVT.ENG.INPUT:
                self.enemies_nbr = int(str(event.get_input()))
                self.add_object(
                    String(5, 0, "You will fight {} enemies".format(self.enemies_nbr))
                )
                self.del_object(self.enemies_obj)
                self.enemies_obj = None
                self.timer = self.new_timer(200)
            else:
                event_to_return.append(event)
        return event_to_return


class SceneSirtet(Scene):
    def __init__(self, game_caller, scene_select):
        super(SceneSirtet, self).__init__("Sirtet")
        self._game_caller = game_caller
        self._scene_select = scene_select
        self.rh: RollerHandler = None
        self.game_started: bool = False

    def setup(self):
        pass

    def activate(self):
        super(SceneSirtet, self).activate()
        if not self.game_started:
            self.rh: RollerHandler = self._game_caller(self._scene_select.enemies_nbr)
            self.add_object(Caller(0, 0, lambda: "Player: {}\n".format(self.rh.player)))
            self.add_object(
                Caller(
                    5, 0, lambda: "Enemy:  {}\n".format(self.rh.enemies[self.rh.ienemy])
                )
            )
            self.add_object(Caller(10, 0, self.rh.bhandler.board_to_render_ascii))
            self.add_object(
                Caller(30, 0, lambda: "{}\n".format(self.rh.matched_row_result))
            )
            self.new_timer(100)
            self.rh.start()
        self.game_started = True

    @update
    def update(self, *events) -> List[Event]:
        event_to_return = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
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
            elif event.evt == EVT.ENG.TIMER:
                self.rh.event_handler(Events.MOVE_DOWN)
            else:
                event_to_return.append(event)
        if self.rh.exit_game:
            event_to_return.append(EventNextScene())
        return event_to_return


class SceneGameOver(Scene):
    def setup(self):
        self.add_object(BoxText(0, 0, "Game Over"))
        self.add_object(FlashText(5, 0, "press 'x' to exit", self.new_timer(50)))

    @update
    def update(self, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            event.exit_on_key("x")
        return event_to_return


def create_game(enemies: int = 2) -> RollerHandler:
    rh = RollerHandler()
    rh.setup(BoardText(), Generator(Segment), Point(0, 4))
    rh.player = Dummy("ME", 100, 1, 100, Warrior(), True)
    rh.enemies = [Dummy("ORC-{}".format(i), 20, 1, 10) for i in range(enemies)]
    return rh


def main():
    h = Handler()
    # game = create_game()
    scene_select = SceneSelect()
    h.add_scene(SceneIntro())
    h.add_scene(scene_select)
    h.add_scene(SceneSirtet(create_game, scene_select))
    h.add_scene(SceneGameOver())
    h.run()


if __name__ == "__main__":
    main()
