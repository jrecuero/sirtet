from typing import Optional, Any, List
import curses
from engine.event import Event, EventInput, Timer, EVT


def update(f):
    def _update(self: "NObject", *events: Event) -> List[Event]:
        if self.enable:
            result = f(self, *events)
            if result is not None:
                return result
        return []

    return _update


def render(f):
    def _render(self: "NObject", screen: Any) -> List[Event]:
        if self.visible:
            result = f(self, screen)
            if result is not None:
                return result
        return []

    return _render


class NObject:
    def __init__(self, y: int, x: int, height: int, width: int):
        self.y: int = y
        self.x: int = x
        self.dy: int = height
        self.dx: int = width
        self.enable: bool = True
        self.visible: bool = True
        self.text_data: str = ""

    def activate(self):
        self.enable = True
        self.visible = True

    def deactivate(self):
        self.enable = False
        self.visible = False

    @update
    def update(self, *events: Event) -> List[Event]:
        return []

    @render
    def render(self, screen) -> List[Event]:
        return []


class String(NObject):
    def __init__(self, y: int, x: int, text_data: str):
        super(String, self).__init__(y, x, 1, len(text_data))
        self.text_data = text_data

    @render
    def render(self, screen) -> List[Event]:
        screen.addstr(self.y, self.x, self.text_data, self.dx)
        return []


class Block(NObject):
    def __init__(self, y: int, x: int, text_data: str):
        super(Block, self).__init__(y, x, 0, 0)
        self.text_data = text_data

    @render
    def render(self, screen) -> List[Event]:
        tokens = self.text_data.split("\n")
        for y, tok in enumerate(tokens):
            screen.addstr(self.y + y, self.x, tok, len(tok))
        return []


class Box(NObject):
    @render
    def render(self, screen) -> List[Event]:
        for x in range(1, self.dx):
            screen.addch(self.y, self.x + x, chr(9473))
        for x in range(1, self.dx):
            screen.addch(self.y + self.dy, self.x + x, chr(9473))
        for y in range(1, self.dy):
            screen.addch(self.y + y, self.x, chr(9475))
        for y in range(1, self.dy):
            screen.addch(self.y + y, self.x + self.dx - 1, chr(9475))
        screen.addch(self.y, self.x, chr(9487))
        screen.addch(self.y + self.dy, self.x, chr(9495))
        screen.addch(self.y, self.x + self.dx - 1, chr(9491))
        screen.addch(self.y + self.dy, self.x + self.dx - 1, chr(9499))
        return []


class BoxText(NObject):
    def __init__(self, y: int, x: int, text_data: str, dy: int = -1, dx: int = -1):
        super(BoxText, self).__init__(y, x, dy, dx)
        self.text_data: str = text_data
        tokens = self.text_data.split("\n")
        if self.dy == -1:
            self.dy = len(tokens) + 1
        if self.dx == -1:
            for t in tokens:
                if len(t) > self.dx:
                    self.dx = len(t)
            self.dx += 2

    @render
    def render(self, screen) -> List[Event]:
        for x in range(1, self.dx):
            screen.addch(self.y, self.x + x, chr(9473))
        for x in range(1, self.dx):
            screen.addch(self.y + self.dy, self.x + x, chr(9473))
        for y in range(1, self.dy):
            screen.addch(self.y + y, self.x, chr(9475))
        for y in range(1, self.dy):
            screen.addch(self.y + y, self.x + self.dx - 1, chr(9475))
        screen.addch(self.y, self.x, chr(9487))
        screen.addch(self.y + self.dy, self.x, chr(9495))
        screen.addch(self.y, self.x + self.dx - 1, chr(9491))
        screen.addch(self.y + self.dy, self.x + self.dx - 1, chr(9499))
        tokens = self.text_data.split("\n")
        for y, tok in enumerate(tokens):
            screen.addstr(self.y + 1 + y, self.x + 1, tok, len(tok))
        return []


class FlashText(String):
    def __init__(self, y: int, x: int, msg: str, t: Timer, on: int = 1, off: int = 1):
        super(FlashText, self).__init__(y, x, msg)
        self.__timer = t
        self.__shadow = msg
        self.__on = on
        self.__on_counter = 0
        self.__off = off
        self.__off_counter = 0

    @update
    def update(self, *events: Event) -> List[Event]:
        for event in events:
            if event.evt == EVT.ENG.TIMER:
                if event.get_timer() == self.__timer:
                    if self.text_data == "":
                        self.__off_counter += 1
                        if self.__off_counter == self.__off:
                            self.__off_counter = 0
                            self.text_data = self.__shadow
                    else:
                        self.__on_counter += 1
                        if self.__on_counter == self.__on:
                            self.__on_counter = 0
                            self.text_data = ""
        return []


class TimeUpdater(String):
    def __init__(self, y: int, x: int, msg: str, t: Timer, caller: Any):
        super(TimeUpdater, self).__init__(y, x, msg)
        self.__timer = t
        self.__caller = caller

    @update
    def update(self, *events: Event) -> List[Event]:
        for event in events:
            if event.evt == EVT.ENG.TIMER:
                if event.get_timer() == self.__timer:
                    self.text_data = self.__caller(self.text_data)
        return []


class Caller(NObject):
    def __init__(self, y: int, x: int, caller: Any):
        super(Caller, self).__init__(y, x, -1, -1)
        self.caller = caller

    @render
    def render(self, screen) -> List[Event]:
        tokens = str(self.caller()).split("\n")
        for y, tok in enumerate(tokens):
            screen.addstr(self.y + y, self.x, tok, len(tok))
        return []


class Input(NObject):
    def __init__(self, y: int, x: int, text_data: str):
        super(Input, self).__init__(y, x, 1, len(text_data))
        self.text_data: str = text_data
        self.input_str: Optional[str] = None

    @render
    def render(self, screen) -> List[Event]:
        screen.addstr(self.y, self.x, self.text_data, self.dx)
        screen.nodelay(False)
        curses.echo()
        self.input_str = screen.getstr(self.y, self.x + self.dx).decode("utf-8")
        screen.nodelay(True)
        curses.noecho()
        return [EventInput(str(self.input_str))]
