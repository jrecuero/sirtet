from typing import Any


class Cell:
    def __init__(self, content: Any):
        self._content = content

    def collision(self, other: "Cell") -> bool:
        return False

    def match(self) -> bool:
        return False

    def update_with(self, other: "Cell") -> None:
        self._content = other._content

    def clone(self) -> "Cell":
        return Cell(self._content)

    def randomize(self) -> "Cell":
        return self

    def __str__(self) -> str:
        return str(self._content)
