from typing import List
import curses
import time
from engine.scene import Scene


class Handler:
    def __init__(self):
        self.screen = None
        self.scenes: List[Scene] = []
        self.iscene: int = -1

    def run(self):
        curses.wrapper(self.__main)

    def __loop(self) -> int:
        key = self.screen.getch()
        curses.flushinp()
        if key == ord("x"):
            exit(0)
        time.sleep(0.01)
        return key

    def __main(self, screen):
        self.screen = screen
        curses.curs_set(False)
        while True:
            self.screen.clear()
            self.update()
            self.render()
            # key = screen.getch()
            # curses.flushinp()
            # if key == ord("x"):
            #     exit(0)
            # time.sleep(0.01)
            self.__loop()

    def init(self):
        pass

    def update(self):
        if self.iscene != -1:
            self.scenes[self.iscene].update()

    def render(self):
        self.screen.addstr(0, 0, "Handler Rendering")
        if self.iscene != -1:
            self.scenes[self.iscene].render()

    def add_scene(self, scn: Scene) -> int:
        self.scenes.append(scn)
        if self.iscene == -1:
            self.iscene = len(self.scenes) - 1
        return len(self.scenes) - 1

    def next_scene(self) -> int:
        self.iscene += 1
        return self.iscene

    def prev_scene(self) -> int:
        self.iscene -= 1
        return self.iscene

    def to_scene(self, iscn: int) -> int:
        self.iscene = iscn
        return self.iscene
