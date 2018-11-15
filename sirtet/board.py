from typing import List
from sirtet.cell import Cell
from sirtet.point import Point
from sirtet.matrix import Mat, Matrix


class Board:
    def __init__(self, mat: Mat = None):
        self.piece_size = 3
        self.arena_width = 9
        self.arena_height = 18
        self.board_width = self.arena_width + 2
        self.board_height = self.arena_height + 1
        self.mat = mat if mat is not None else self.default_mat()

    def new_cell_empty(self) -> Cell:
        raise Exception("Abstract class")

    def new_cell_border(self) -> Cell:
        raise Exception("Abstract class")

    def _new_row(self) -> List[Cell]:
        row: List[Cell] = []
        row.append(self.new_cell_border())
        for _ in range(self.arena_width):
            row.append(self.new_cell_empty())
        row.append(self.new_cell_border())
        return row

    def _new_bottom_row(self) -> List[Cell]:
        row: List[Cell] = []
        for _ in range(self.board_width):
            row.append(self.new_cell_border())
        return row

    def default_mat(self) -> Mat:
        mat = Mat([])
        for _ in range(self.board_height - 1):
            mat.append(self._new_row())
        mat.append(self._new_bottom_row())
        return mat

    def clone(self) -> "Board":
        b = self.__class__(Mat([]))
        for x in range(self.board_height):
            b.mat.append([])
            for y in range(self.board_width):
                b.mat[x].append(self.mat[x][y].clone())
        return b

    def get_mat(self) -> Mat:
        return self.mat

    def set_mat(self, mat: Mat) -> None:
        if len(mat) != self.board_height or len(mat[0]) != self.board_width:
            assert False, "board wrong matrix dimension: ({}, {})".format(
                len(mat), len(mat) and len(mat[0])
            )
        self.mat = mat

    def get_matrix_at(self, pos: Point) -> Matrix:
        mat = Mat([])
        x, y = pos.x, pos.y
        for i in range(x, x + self.piece_size):
            mat.append(self.mat[i][y : y + self.piece_size])
        return Matrix(mat)

    def update_with_matrix_at(self, mat: Matrix, pos: Point) -> None:
        x, y = pos.x, pos.y
        for xi, row in enumerate(mat.get_mat()):
            for yi, col in enumerate(row):
                if not self.mat[x + xi][y + yi].match() and col.match():
                    self.mat[x + xi][y + yi] = col
                # self.mat[x + xi][y + yi].update_with(col)

    def clear_with_matrix_at(self, mat: Matrix, pos: Point) -> None:
        x, y = pos.x, pos.y
        for xi, row in enumerate(mat.get_mat()):
            for yi, col in enumerate(row):
                self.mat[x + xi][y + yi] = self.new_cell_empty()

    def get_arena_for_row(self, row: List[Cell]) -> List[Cell]:
        return row[1 : self.board_width - 1]

    def get_arena_for_row_index(self, index: int) -> List[Cell]:
        return self.get_arena_for_row(self.mat[index])

    def check_for_match_row_at(self, row: int) -> bool:
        # arena for matching rows does not include board borders.
        #
        # for col in range(1, self.board_width):
        #     if not self.mat[row][col].match():
        for col in self.get_arena_for_row(self.mat[row]):
            if not col.match():
                return False
        return True

    def check_for_match_row(self) -> List[int]:
        result: List[int] = []
        for irow in range(self.board_height - 1):
            if self.check_for_match_row_at(irow):
                result.append(irow)
        return result

    def remove_rows(self, irows: List[int]) -> None:
        result = Mat([])
        for _ in range(len(irows)):
            result.append(self._new_row())
        for irow, row in enumerate(self.mat):
            if irow not in irows:
                result.append(row)
        self.set_mat(result)

    def __str__(self) -> str:
        return "\n".join([" ".join(str(_) for _ in row) for row in self.mat])

    def render(self) -> None:
        for row in self.mat:
            for cell in row:
                cell.render()
