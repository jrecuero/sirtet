from typing import Any, List, Optional
import curses
import time
from engine.scene import Scene
from engine.event import Timer, Event, EventKey, EventTimer


class Handler:
    def __init__(self, tick: float = 0.01):
        self.screen: Any = None
        self.scenes: List[Scene] = []
        self.iscene: int = -1
        self.key: int = -1
        self.tick: float = tick
        self.timers: List[Timer] = []
        self.render_events: List[Event] = []

    def run(self):
        curses.wrapper(self.__main)

    def __loop(self) -> int:
        time.sleep(self.tick)
        self.key = self.screen.getch()
        curses.flushinp()
        return self.key

    def __main(self, screen: Any):
        self.screen = screen
        self.screen.nodelay(True)
        curses.curs_set(False)
        while True:
            self.screen.clear()
            self.update()
            self.render()
            self.__loop()

    def new_timer(self, timeout: int, enable: bool = True) -> Timer:
        t = Timer(timeout, enable)
        return self.add_timer(t)

    def add_timer(self, t: Timer) -> Timer:
        self.timers.append(t)
        return t

    def del_timer(self, t: Timer) -> None:
        self.timers.remove(t)

    def new_scene(self) -> Scene:
        scn = Scene()
        return self.add_scene(scn)

    def add_scene(self, scn: Scene) -> Scene:
        scn.setup()
        self.scenes.append(scn)
        if self.iscene == -1:
            self.iscene = len(self.scenes) - 1
        return scn

    def del_scene(self, scn: Scene) -> None:
        self.scenes.remove(scn)

    def next_scene(self) -> int:
        self.iscene += 1
        return self.iscene

    def prev_scene(self) -> int:
        self.iscene -= 1
        return self.iscene

    def get_scene(self) -> Optional[Scene]:
        if self.iscene != -1:
            return self.scenes[self.iscene]
        return None

    def to_scene(self, scn: Scene) -> Optional[Scene]:
        for i, s in enumerate(self.scenes):
            if s == scn:
                self.iscene = i
                return s
        return None

    def setup(self):
        pass

    def update(self):
        if self.iscene != -1:
            events = []
            events.extend(self.render_events)
            if self.key != -1:
                events.append(EventKey(self.key))
                self.key = -1
            for t in self.timers:
                if t.inc():
                    events.append(EventTimer(t))
            self.scenes[self.iscene].update(*events)

    def render(self):
        if self.iscene != -1:
            self.render_events = self.scenes[self.iscene].render(self.screen)
