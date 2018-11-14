import random
from typing import List, Any, cast
from sirtet.cell import Cell
from sirtet.logics.roller.spores import Null, Damage, Life, Skill


class Segment(Cell):
    def __init__(self, content: Any):
        super(Segment, self).__init__(content)
        if isinstance(content, int):
            if content == 1:
                self._content = Damage()
            else:
                self._content = Null()
        else:
            self._content = content

    def match(self) -> bool:
        return self._content.match()

    def update_with(self, other: "Cell") -> None:
        if not self._content.match():
            self._content = other._content

    def randomize(self) -> "Cell":
        spores: List[Any] = (
            cast(List[Any], [Damage]) * 7
            + cast(List[Any], [Life]) * 2
            + cast(List[Any], [Skill])
        )
        if self.match():
            self._content = spores[random.randint(0, len(spores) - 1)]()
        else:
            self._content = Null()
        return self

    def __str__(self) -> str:
        return str(self._content)
        # elif self._content == 1:
        #     return chr(12872)
        # elif self._content == 2:
        #     return chr(12872)
        # return str(self._content)
        # return chr(9209)
        # return chr(9210)
        # return chr(9208)
