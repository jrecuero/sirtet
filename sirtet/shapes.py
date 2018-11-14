import random
from typing import List, Callable, Union, Any
from sirtet.cell import Cell
from sirtet.matrix import Mat, Matrix


class Shapes:
    def __init__(self, cell_klass: Callable[..., Cell]):
        self.cell: Callable[..., Cell] = cell_klass
        self._patterns: List[List[List[int]]] = [
            [[0, 0, 0], [1, 1, 0], [0, 1, 1]],
            [[0, 0, 0], [0, 1, 1], [1, 1, 0]],
            [[1, 0, 0], [1, 0, 0], [1, 1, 0]],
            [[0, 0, 1], [0, 0, 1], [0, 1, 1]],
            [[1, 0, 0], [1, 0, 0], [1, 1, 1]],
            [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
            [[1, 1, 1], [0, 0, 1], [1, 1, 1]],
            [[0, 0, 1], [0, 1, 1], [0, 0, 1]],
            [[0, 0, 1], [1, 1, 1], [0, 0, 1]],
            [[1, 0, 1], [0, 1, 1], [0, 0, 1]],
            [[0, 0, 1], [0, 1, 1], [1, 0, 1]],
            [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
            [[1, 1, 0], [1, 1, 0], [1, 1, 0]],
            [[1, 1, 1], [1, 1, 0], [1, 1, 0]],
            [[1, 1, 0], [1, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [1, 1, 0], [1, 1, 1]],
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
            [[1, 1, 0], [1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 0], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 1], [1, 1, 0]],
            [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
            [[0, 0, 0], [1, 1, 0], [0, 0, 0]],
            [[1, 0, 0], [1, 1, 0], [0, 0, 0]],
            [[0, 0, 0], [1, 1, 0], [1, 0, 0]],
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        ]

        def _new_mat(mat: Mat):
            def __new_mat():
                return mat

            return __new_mat

        # self._shapes: List[Callable[[], Mat]] = []
        # for entry in self._patterns:
        #     trav = []
        #     for row in entry:
        #         tmp = []
        #         for col in row:
        #             tmp.append(self.cell(col))
        #         trav.append(tmp)
        #     self._shapes.append(_new_mat(Mat(trav)))
        self._shapes: List[Callable[[], Mat]] = [
            _new_mat(Mat([[self.cell(col) for col in row] for row in entry]))
            for entry in self._patterns
        ]

    def dim(self) -> int:
        return len(self._shapes)

    def get(self, index: int = None) -> Mat:
        index = random.randint(0, self.dim() - 1) if index is None else index
        return self._shapes[index]()


class Generator:
    def __init__(self, cell_klass: Callable[..., Cell]):
        self.shapes: Shapes = Shapes(cell_klass)

    def get_next(self) -> Matrix:
        # return Matrix(self.shapes.get())

        # mat = self.shapes.get()
        # for row in mat:
        #     for col in row:
        #         col.randomize()
        # return Matrix(mat)

        return Matrix(self.shapes.get()).randomize()


# if __name__ == "__main__":
#     from sirtet.assets.cells import Segment

#     s = Shapes(Segment)
#     for x in s._shapes:
#         print(Matrix(x()))
#         print()
