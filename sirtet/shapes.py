import random
from typing import List, Callable, Union
from sirtet.cell import Cell, Segment
from sirtet.matrix import Mat, Matrix


class Shapes:

    # def __init__(self, cell_klass: Callable[..., Cell]=None):
    #     self.cell: Union[Callable[..., Any], Segment] = cell_klass if cell_klass is not None else Segment
    def __init__(self, cell_klass=None):
        self.cell = cell_klass if cell_klass is not None else Segment
        self._shapes: List[Callable[[], Mat]] = [lambda: Mat([[self.cell(0), self.cell(0), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(0)],
                                                              [self.cell(0), self.cell(1), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(0), self.cell(0), self.cell(0)],
                                                              [self.cell(0), self.cell(1), self.cell(1)],
                                                              [self.cell(1), self.cell(1), self.cell(0)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(0), self.cell(0)],
                                                              [self.cell(1), self.cell(0), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(0)], ]),
                                                 lambda: Mat([[self.cell(0), self.cell(0), self.cell(1)],
                                                              [self.cell(0), self.cell(0), self.cell(1)],
                                                              [self.cell(0), self.cell(1), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(0), self.cell(0)],
                                                              [self.cell(1), self.cell(0), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(0), self.cell(0), self.cell(1)],
                                                              [self.cell(0), self.cell(0), self.cell(1)],
                                                              [self.cell(1), self.cell(1), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(1), self.cell(1)],
                                                              [self.cell(0), self.cell(0), self.cell(1)],
                                                              [self.cell(1), self.cell(1), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(0), self.cell(0), self.cell(1)],
                                                              [self.cell(0), self.cell(1), self.cell(1)],
                                                              [self.cell(0), self.cell(0), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(0), self.cell(0), self.cell(1)],
                                                              [self.cell(1), self.cell(1), self.cell(1)],
                                                              [self.cell(0), self.cell(0), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(0), self.cell(1)],
                                                              [self.cell(0), self.cell(1), self.cell(1)],
                                                              [self.cell(0), self.cell(0), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(0), self.cell(0), self.cell(1)],
                                                              [self.cell(0), self.cell(1), self.cell(1)],
                                                              [self.cell(1), self.cell(0), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(0), self.cell(1), self.cell(0)],
                                                              [self.cell(0), self.cell(1), self.cell(0)],
                                                              [self.cell(0), self.cell(1), self.cell(0)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(1), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(0)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(1), self.cell(1)],
                                                              [self.cell(1), self.cell(1), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(0)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(1), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(1)],
                                                              [self.cell(1), self.cell(1), self.cell(0)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(1), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(0), self.cell(0)],
                                                              [self.cell(0), self.cell(1), self.cell(0)],
                                                              [self.cell(0), self.cell(0), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(0), self.cell(1)],
                                                              [self.cell(0), self.cell(1), self.cell(0)],
                                                              [self.cell(1), self.cell(0), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(1), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(1)],
                                                              [self.cell(1), self.cell(1), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(1), self.cell(1)],
                                                              [self.cell(1), self.cell(1), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(1)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(1), self.cell(1)],
                                                              [self.cell(1), self.cell(1), self.cell(1)],
                                                              [self.cell(1), self.cell(1), self.cell(0)], ]),
                                                 lambda: Mat([[self.cell(0), self.cell(0), self.cell(0)],
                                                              [self.cell(0), self.cell(1), self.cell(0)],
                                                              [self.cell(0), self.cell(0), self.cell(0)], ]),
                                                 lambda: Mat([[self.cell(0), self.cell(0), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(0)],
                                                              [self.cell(0), self.cell(0), self.cell(0)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(0), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(0)],
                                                              [self.cell(0), self.cell(0), self.cell(0)], ]),
                                                 lambda: Mat([[self.cell(0), self.cell(0), self.cell(0)],
                                                              [self.cell(1), self.cell(1), self.cell(0)],
                                                              [self.cell(1), self.cell(0), self.cell(0)], ]),
                                                 lambda: Mat([[self.cell(1), self.cell(1), self.cell(1)],
                                                              [self.cell(1), self.cell(1), self.cell(1)],
                                                              [self.cell(1), self.cell(1), self.cell(1)], ]), ]

    def dim(self) -> int:
        return len(self._shapes)

    def get(self, index: int=None) -> Mat:
        index = random.randint(0, self.dim() - 1) if index is None else index
        return self._shapes[index]()


class Generator:

    def __init__(self):
        self.shapes: Shapes = Shapes()

    def get_next(self) -> Matrix:
        return Matrix(self.shapes.get())


if __name__ == '__main__':
    s = Shapes()
    for x in s._shapes:
        print(Matrix(x()))
        print()
