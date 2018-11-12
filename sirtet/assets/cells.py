from typing import Any
from sirtet.cell import Cell


class Int(Cell):
    def __init__(self, content: Any):
        super(Int, self).__init__(content)

    def match(self) -> bool:
        return self._content != 0

    def collision(self, other: Cell) -> bool:
        return self.match() and other.match()

    def update_with(self, other: "Cell") -> None:
        if self._content == 0:
            self._content = other._content

    def clone(self) -> "Cell":
        return Int(self._content)

    def __str__(self) -> str:
        if self._content == 0:
            return "."
        # return str(self._content)
        # return chr(9608)
        return chr(9209)


class Segment(Int):
    def __init__(self, content: Any):
        super(Segment, self).__init__(content)

    def clone(self) -> "Cell":
        return Segment(self._content)

    def __str__(self) -> str:
        if self._content == 0:
            return "_"
        return str(self._content)
        # elif self._content == 1:
        #     return chr(12872)
        # elif self._content == 2:
        #     return chr(12872)
        # return str(self._content)
        # return chr(9209)
        # return chr(9210)
        # return chr(9208)
