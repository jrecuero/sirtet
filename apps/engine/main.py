from typing import List
from engine.nobject import Box, String, Block, Input, BoxText
from engine.event import Event, EventNextScene
from engine.event import EVT_ENG_KEY, EVT_ENG_TIMER, EVT_ENG_INPUT
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
        self.add_object(Box(0, 0, 2, len("Engine Example") + 2))
        self.add_object(String(1, 1, "Engine Example"))
        self.input_obj = Input(3, 0, "Name: ")
        self.add_object(self.input_obj)

    @update
    def update(self, *events: Event) -> List[Event]:
        event_to_return = []
        for event in events:
            if event.evt == EVT_ENG_KEY:
                key = event.get_key()
                if key is not None:
                    if key == ord("x"):
                        exit(0)
                    elif key == ord("1"):
                        self.tmp[0] = Block(6, 0, "Line #1\nLine #2\nLine #3")
                        self.add_object(self.tmp[0])
                    elif key == ord("2"):
                        self.tmp[1] = Block(6, 10, "Jose Carlos\nRecuero Arias\n51")
                        self.add_object(self.tmp[1])
                    elif key == ord("3"):
                        if self.tmp[0] is not None:
                            self.del_object(self.tmp[0])
                            self.tmp[0] = None
                    elif key == ord("4"):
                        if self.tmp[1] is not None:
                            self.del_object(self.tmp[1])
                            self.tmp[1] = None
                    elif key == ord("z"):
                        self.enable = False
                    elif key == ord("n"):
                        event_to_return.append(EventNextScene())
            elif event.evt == EVT_ENG_TIMER:
                self.t_counter += 1
                self.add_object(
                    String(9, 0, "Timeout expired: {}".format(self.t_counter))
                )
            elif event.evt == EVT_ENG_INPUT:
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
        self.add_object(String(0, 0, "last page"))

    @update
    def update(self, *events: Event) -> List[Event]:
        event_to_return = []
        for event in events:
            if event.evt == EVT_ENG_KEY:
                key = event.get_key()
                if key is not None:
                    if key == ord("x"):
                        exit(0)
        return event_to_return


if __name__ == "__main__":
    h = Handler()
    h.add_scene(SceneMain())
    h.add_scene(SceneLast())
    h.run()
