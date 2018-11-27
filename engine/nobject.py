from typing import Optional, Any


class NObject:
    def __init__(self, y: int, x: int, height: int, width: int):
        self.y: int = y
        self.x: int = x
        self.dy: int = height
        self.dx: int = width

    def update(self):
        pass

    def render(self, screen):
        pass


class String(NObject):
    def __init__(self, y: int, x: int, message: str):
        super(String, self).__init__(y, x, 1, len(message))
        self.message = message

    def render(self, screen):
        screen.addstr(self.y, self.x, self.message, self.dx)


class Block(NObject):
    def __init__(self, y: int, x: int, block: str):
        super(Block, self).__init__(y, x, 0, 0)
        self.block = block

    def render(self, screen: Any):
        tokens = self.block.split("\n")
        for y, tok in enumerate(tokens):
            screen.addstr(self.y + y, self.x, tok, len(tok))


class Box(NObject):
    def render(self, screen: Any):
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


class Caller(NObject):
    def __init__(self, y: int, x: int, caller: Any):
        super(Caller, self).__init__(y, x, -1, -1)
        self.caller = caller

    def render(self, screen: Any):
        tokens = str(self.caller()).split("\n")
        for y, tok in enumerate(tokens):
            screen.addstr(self.y + y, self.x, tok, len(tok))


class Input(NObject):
    def __init__(self, y: int, x: int, message: str):
        super(Input, self).__init__(y, x, 1, len(message))
        self.message: str = message
        self.input: Optional[str] = None

    def render(self, screen: Any):
        screen.addstr(self.y, self.x, self.message, self.dx)
        self.input = screen.getstr(self.y, self.x + self.dx)
