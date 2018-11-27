from typing import Any, List, Optional
import curses
import time
from engine.scene import Scene

EVT_ENG_KEY: int = 100
EVT_ENG_TIMER: int = 200


class Timer:
    def __init__(self, timeout: int):
        self.timeout: int = timeout
        self.__counter: int = 0
        self.__enable: bool = False

    def enable(self) -> None:
        self.__enable = True

    def disable(self) -> None:
        self.__enable = False

    def inc(self) -> bool:
        if self.enable:
            self.__counter += 1
            if self.__counter >= self.timeout:
                self.__counter = 0
                return True
        return False


class Event:
    def __init__(self, evt: int, **kwargs):
        self.evt = evt
        self.params = kwargs

    def get_key(self) -> Optional[int]:
        if self.evt == EVT_ENG_KEY:
            return self.params.get("key", None)
        return None

    def get_timer(self) -> Optional[Timer]:
        if self.evt == EVT_ENG_TIMER:
            return self.params.get("timer", None)
        return None


class EventKey(Event):
    def __init__(self, key: int):
        super(EventKey, self).__init__(EVT_ENG_KEY, key=key)


class EventTimer(Event):
    def __init__(self, t: Timer):
        super(EventTimer, self).__init__(EVT_ENG_TIMER, timer=t)


class Handler:
    def __init__(self, tick: float = 0.01):
        self.screen: Any = None
        self.scenes: List[Scene] = []
        self.iscene: int = -1
        self.key: int = -1
        self.tick: float = tick
        self.timers: List[Timer] = []

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

    def new_timer(self, timeout: int) -> Timer:
        t = Timer(timeout)
        self.timers.append(t)
        return t

    def del_timer(self, t: Timer) -> None:
        self.timers.remove(t)

    def new_scene(self) -> Scene:
        scn = Scene()
        return self.add_scene(scn)

    def add_scene(self, scn: Scene) -> Scene:
        self.scenes.append(scn)
        if self.iscene == -1:
            self.iscene = len(self.scenes) - 1
        return scn

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

    def del_scene(self, scn: Scene) -> None:
        self.scenes.remove(scn)

    def init(self):
        pass

    def update(self):
        if self.iscene != -1:
            events = []
            if self.key != -1:
                events.append(EventKey(self.key))
                self.key = -1
            for t in self.timers:
                if t.inc():
                    events.append(EventTimer(t))
            self.scenes[self.iscene].update(*events)

    def render(self):
        if self.iscene != -1:
            self.scenes[self.iscene].render(self.screen)
