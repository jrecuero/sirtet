from typing import Any
from sirtet.cell import Cell


class Int(Cell):
    def __init__(self, content: Any):
        super(Int, self).__init__(content)

    def match(self) -> bool:
        return self._content != 0

    def update_with(self, other: "Cell") -> None:
        if not self.match():
            self._content = other._content

    def equal(self, other: Any) -> bool:
        return self._content == other

    def __str__(self) -> str:
        return str(self._content)


class Block(Int):
    def __init__(self, content: Any):
        super(Block, self).__init__(content)

    def __str__(self) -> str:
        if self._content == 0:
            # return "."
            # return "  "
            return " "
        # return str(self._content)
        # return chr(9608)
        # return "{}{}".format(chr(9608), chr(9608))
        return "{}".format(chr(9608))
        # return chr(9209)
