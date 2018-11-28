from engine.nobject import Box, String, Block, Input, BoxText
from engine.event import Event, EVT_ENG_KEY, EVT_ENG_TIMER, EVT_ENG_INPUT
from engine.handler import Handler
from engine.scene import Scene


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
        self.timer = h.new_timer(100)

    def update(self, *events: Event):
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


if __name__ == "__main__":
    h = Handler()
    h.add_scene(SceneMain())
    h.run()
