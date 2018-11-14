from typing import Any


class Cell:
    def __init__(self, content: Any):
        self._content: Any = content

    def match(self) -> bool:
        return False

    def collision(self, other: "Cell") -> bool:
        return self.match() and other.match()

    def update_with(self, other: "Cell") -> None:
        self._content = other._content

    def clone(self) -> "Cell":
        return self.__class__(self._content)

    def randomize(self) -> "Cell":
        return self

    def __str__(self) -> str:
        return str(self._content)

    def render(self) -> None:
        pass

    def to_string(self) -> str:
        return self._content.to_string()
