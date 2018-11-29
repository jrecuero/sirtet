from typing import List
from engine.nobject import Box, String, Block, Input, BoxText, FlashText, TimeUpdater
from engine.event import Event, EventNextScene, EVT, KeyHandler
from engine.handler import Handler
from engine.scene import Scene, update


class SceneMain(Scene):
    def __init__(self):
        super(SceneMain, self).__init__()
        self.tmp = [None, None]
        self.timer = None
        self.t_counter = 0
        self.input_obj = None

    def setup(self):
        def handle_1():
            self.tmp[0] = Block(6, 0, "Line #1\nLine #2\nLine #3")
            self.add_object(self.tmp[0])
            return []

        def handle_2():
            self.tmp[1] = Block(6, 10, "Jose Carlos\nRecuero Arias\n51")
            self.add_object(self.tmp[1])
            return []

        def handle_3():
            if self.tmp[0] is not None:
                self.del_object(self.tmp[0])
                self.tmp[0] = None
            return []

        def handle_4():
            if self.tmp[1] is not None:
                self.del_object(self.tmp[1])
                self.tmp[1] = None
            return []

        def handle_t():
            self.timer.enable = not self.timer.enable
            return []

        def handle_z():
            self.enable = False
            return []

        def handle_n():
            return [EventNextScene()]

        self.add_object(Box(0, 0, 2, len("Engine Example") + 2))
        self.add_object(String(1, 1, "Engine Example"))
        self.input_obj = Input(3, 0, "Name: ")
        self.add_object(self.input_obj)
        self.kh = KeyHandler(
            {
                "x": lambda: exit(0),
                "1": handle_1,
                "2": handle_2,
                "3": handle_3,
                "4": handle_4,
                "t": handle_t,
                "z": handle_z,
                "n": lambda: [EventNextScene()],
            }
        )

    @update
    def update(self, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            if event.evt == EVT.ENG.KEY:
                event_to_return.extend(self.kh.update(event))
            elif event.evt == EVT.ENG.TIMER:
                if event.get_timer() == self.timer:
                    self.t_counter += 1
                    self.add_object(
                        String(9, 0, "Timeout expired: {}".format(self.t_counter))
                    )
            elif event.evt == EVT.ENG.INPUT:
                msg = event.get_input()
                self.add_object(BoxText(3, 0, "Your name is {}".format(msg)))
                self.del_object(self.input_obj)
                self.input_obj = None
                self.timer = self.new_timer(100)
            else:
                event_to_return.append(event)
        return event_to_return


class SceneLast(Scene):
    def setup(self):
        def updater(message: str) -> str:
            if message == "@copyright":
                return "by jose carlos"
            elif message == "by jose carlos":
                return "San Jose, 2018"
            elif message == "San Jose, 2018":
                return ""
            else:
                return "@copyright"

        self.add_object(FlashText(0, 0, "last page", self.new_timer(50), on=1, off=1))
        self.add_object(TimeUpdater(1, 0, "@copyright", self.new_timer(100), updater))

    @update
    def update(self, *events: Event) -> List[Event]:
        event_to_return: List[Event] = []
        for event in events:
            event.exit_on_key("x")
        return event_to_return


if __name__ == "__main__":
    h = Handler()
    h.add_scene(SceneMain())
    h.add_scene(SceneLast())
    h.run()
