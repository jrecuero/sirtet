from typing import Any


class Cell:
    def __init__(self, content: Any):
        self._content: Any = content

    @property
    def content(self) -> Any:
        return self._content

    def equal(self, content: Any) -> bool:
        return self._content.equal(content)

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

    def render_ascii(self, screen: Any) -> None:
        screen.addstr("{}".format(self))

    def to_string(self) -> str:
        return self._content.to_string()
