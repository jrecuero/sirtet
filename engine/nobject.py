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


class Box(NObject):
    def render(self, screen):
        screen.addch(self.y, self.x, "|")
        screen.hline(self.y, self.x + 1, "-", self.dx - 2)
        screen.addch(self.y, self.x + self.dx - 1, "|")
        screen.vline(self.y + 1, self.x, "|", self.dy - 2)
        screen.vline(self.y + 1, self.x + self.dx - 1, "|", self.dy - 2)
        screen.addch(self.y + self.dy - 1, self.x, "|")
        screen.hline(self.y + self.dy - 1, self.x + 1, "-", self.dx - 2)
        screen.addch(self.y + self.dy - 1, self.x + self.dx - 1, "|")
