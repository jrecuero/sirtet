class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move_left(self) -> "Point":
        return Point(self.x, self.y - 1)

    def move_right(self) -> "Point":
        return Point(self.x, self.y + 1)

    def move_down(self) -> "Point":
        return Point(self.x + 1, self.y)

    def __str__(self) -> str:
        return "({}, {})".format(self.x, self.y)
