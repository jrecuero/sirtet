from typing import NewType, List, Tuple
from sirtet.cell import Cell

Mat = NewType("Mat", List[List[Cell]])


class Matrix:
    def __init__(self, m: Mat):
        self.mat: Mat = Mat([])
        self.dim = 3
        self.set_mat(m)

    def _check(self, m: Mat) -> bool:
        if m is None or len(m) != self.dim or len(m[0]) != self.dim:
            return False
        return True

    def get_mat(self) -> Mat:
        return self.mat

    def set_mat(self, m: Mat) -> None:
        if not self._check(m):
            assert False, "wrong matrix dimension: {}".format(m)
        self.mat = Mat(m[:])

    def get_dim(self) -> Tuple:
        return len(self.mat), len(self.mat[0])

    def rotate_clockwise(self) -> "Matrix":
        """Rotate nxn matrix by 90 degrees clockwise.
        """
        # result matrix
        result = Mat([row[:] for row in self.mat])
        m = len(self.mat[0])
        for x in range(0, m):
            for j in range(0, m):
                result[j][m - 1 - x] = self.mat[x][j]
        return Matrix(result)

    def rotate_anticlockwise(self) -> "Matrix":
        """Rotate nxn matrix by 90 degrees anti-clockwise.
        """
        # result matrix
        result = Mat([row[:] for row in self.mat])
        m = len(self.mat[0])
        for x in range(0, m):
            for j in range(0, m):
                result[x][j] = self.mat[j][m - 1 - x]
        return Matrix(result)

    def get_collisions_with(self, mat: Mat) -> List[Tuple]:
        if not self._check(mat):
            assert False, "wrong matrix dimension: {}".format(mat)
        m = len(self.mat[0])
        collisions: List[Tuple] = []
        for x in range(m):
            for y in range(m):
                if self.mat[x][y].collision(mat[x][y]):
                    collisions.append((x, y))
        return collisions

    def is_collision_with(self, mat: Mat) -> bool:
        return len(self.get_collisions_with(mat)) != 0

    def is_bottom_collision_with(self, mat: Mat) -> bool:
        collisions = self.get_collisions_with(mat)
        m = len(self.mat)
        for entry in collisions:
            if entry[0] == (m - 1):
                return True
        return False

    def randomize(self) -> "Matrix":
        for row in self.mat:
            for col in row:
                col.randomize()
        return self

    def __str__(self) -> str:
        return "\n".join([" ".join(str(_) for _ in row) for row in self.mat])
