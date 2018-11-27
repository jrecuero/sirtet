from engine.nobject import Box, String, Block
from engine.handler import Handler, EVT_ENG_KEY, EVT_ENG_TIMER
from engine.scene import Scene


class SceneMain(Scene):
    def __init__(self):
        super(SceneMain, self).__init__()
        self.tmp = [None, None]
        self.timer = None
        self.t_counter = 0

    def update(self, *events):
        if len(events) and events[0].evt == EVT_ENG_KEY:
            key = events[0].get_key()
            if key is not None:
                if key == ord("x"):
                    exit(0)
                elif key == ord("1"):
                    self.tmp[0] = Block(3, 0, "Line #1\nLine #2\nLine #3")
                    self.add_object(self.tmp[0])
                elif key == ord("2"):
                    self.tmp[1] = Block(3, 10, "Jose Carlos\nRecuero Arias\n51")
                    self.add_object(self.tmp[1])
                elif key == ord("3"):
                    if self.tmp[0] is not None:
                        self.del_object(self.tmp[0])
                        self.tmp[0] = None
                elif key == ord("4"):
                    if self.tmp[1] is not None:
                        self.del_object(self.tmp[1])
                        self.tmp[1] = None
        elif len(events) and events[0].evt == EVT_ENG_TIMER:
            self.t_counter += 1
            self.add_object(String(6, 0, "Timeout expired: {}".format(self.t_counter)))


if __name__ == "__main__":
    h = Handler()
    scn = SceneMain()
    scn.add_object(Box(0, 0, 2, len("Engine Example") + 2))
    scn.add_object(String(1, 1, "Engine Example"))
    # scn.add_object(Block(3, 0, "Line #1\nLine #2\nLine #3"))
    # scn.add_object(Block(3, 10, "Jose Carlos\nRecuero Arias\n51"))
    h.add_scene(scn)
    scn.timer = h.new_timer(100)
    h.run()
