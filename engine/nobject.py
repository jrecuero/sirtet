from typing import Optional, Any, List
import curses
from engine.event import Event, EventInput


class NObject:
    def __init__(self, y: int, x: int, height: int, width: int):
        self.y: int = y
        self.x: int = x
        self.dy: int = height
        self.dx: int = width

    def update(self):
        pass

    def render(self, screen) -> List[Event]:
        return []


class String(NObject):
    def __init__(self, y: int, x: int, message: str):
        super(String, self).__init__(y, x, 1, len(message))
        self.message = message

    def render(self, screen) -> List[Event]:
        screen.addstr(self.y, self.x, self.message, self.dx)
        return []


class Block(NObject):
    def __init__(self, y: int, x: int, block: str):
        super(Block, self).__init__(y, x, 0, 0)
        self.block = block

    def render(self, screen) -> List[Event]:
        tokens = self.block.split("\n")
        for y, tok in enumerate(tokens):
            screen.addstr(self.y + y, self.x, tok, len(tok))
        return []


class Box(NObject):
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
    def __init__(self, y: int, x: int, message: str, dy: int = -1, dx: int = -1):
        super(BoxText, self).__init__(y, x, dy, dx)
        self.message: str = message
        tokens = self.message.split("\n")
        if self.dy == -1:
            self.dy = len(tokens) + 1
        if self.dx == -1:
            for t in tokens:
                if len(t) > self.dx:
                    self.dx = len(t)
            self.dx += 2

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
        tokens = self.message.split("\n")
        for y, tok in enumerate(tokens):
            screen.addstr(self.y + 1 + y, self.x + 1, tok, len(tok))
        return []


class Caller(NObject):
    def __init__(self, y: int, x: int, caller: Any):
        super(Caller, self).__init__(y, x, -1, -1)
        self.caller = caller

    def render(self, screen) -> List[Event]:
        tokens = str(self.caller()).split("\n")
        for y, tok in enumerate(tokens):
            screen.addstr(self.y + y, self.x, tok, len(tok))
        return []


class Input(NObject):
    def __init__(self, y: int, x: int, message: str):
        super(Input, self).__init__(y, x, 1, len(message))
        self.message: str = message
        self.input_str: Optional[str] = None

    def render(self, screen) -> List[Event]:
        screen.addstr(self.y, self.x, self.message, self.dx)
        screen.nodelay(False)
        curses.echo()
        self.input_str = screen.getstr(self.y, self.x + self.dx).decode("utf-8")
        screen.nodelay(True)
        curses.noecho()
        return [EventInput(str(self.input_str))]
