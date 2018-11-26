from engine.nobject import Box
from engine.handler import Handler

if __name__ == "__main__":
    h = Handler()
    b = Box(0, 0, 10, 30)
    scn, iscn = h.new_scene()
    scn.add_object(b)
    h.run()
