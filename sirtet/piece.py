from sirtet.point import Point
from sirtet.matrix import Matrix


class Piece:
    def __init__(self):
        self.matrix = None
        self.pos = None

    def move_left(self) -> Point:
        return self.pos.move_left()

    def move_right(self) -> Point:
        return self.pos.move_right()

    def move_down(self) -> Point:
        return self.pos.move_down()

    def rotate_clockwise(self) -> Matrix:
        return self.matrix.rotate_clockwise()

    def rotate_anticlockwise(self) -> Matrix:
        return self.matrix.rotate_anticlockwise()
