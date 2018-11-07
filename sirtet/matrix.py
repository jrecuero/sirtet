from typing import List, Tuple, Any, NewType


class Cell:

    def __init__(self, content: Any):
        self._content = content

    def collision(self, other: 'Cell') -> bool:
        pass

    def match(self) -> bool:
        pass

    def __str__(self) -> str:
        pass


class Int(Cell):

    def __init__(self, content: Any):
        super(Int, self).__init__(content)

    def match(self) -> bool:
        return self._content != 0

    def collision(self, other: Cell) -> bool:
        return self.match() and other.match()

    def __str__(self) -> str:
        return str(self._content)


Mat = NewType('Mat', List[List[Cell]])


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
            assert False, 'wrong matrix dimension: {}'.format(m)
        self.mat = Mat(m[:])

    def get_dim(self) -> Tuple:
        return len(self.mat), len(self.mat[0])

    def rotate_clockwise(self) -> 'Matrix':
        """Rotate nxn matrix by 90 degrees clockwise.
        """
        #result matrix
        result = Mat([row[:] for row in self.mat])
        m = len(self.mat[0])
        for x in range(0, m):
            for j in range(0, m):
                result[j][m - 1 - x] = self.mat[x][j]
        return Matrix(result)

    def rotate_anticlockwise(self) -> 'Matrix':
        """Rotate nxn matrix by 90 degrees anti-clockwise.
        """
        #result matrix
        result = Mat([row[:] for row in self.mat])
        m = len(self.mat[0])
        for x in range(0, m):
            for j in range(0, m):
                result[x][j] = self.mat[j][m - 1 - x]
        return Matrix(result)

    def get_collisions_with(self, mat: Mat) -> List[Tuple]:
        if not self._check(mat):
            assert False, 'wrong matrix dimension: {}'.format(mat)
        m = len(self.mat[0])
        collisions: List[Tuple] = []
        for x in range(m):
            for y in range(m):
                if self.mat[x][y].collision(mat[x][y]):
                    collisions.append((x, y))
        return collisions

    def is_collision_with(self, mat: Mat) -> bool:
        return self.get_collisions_with(mat) != 0

    def is_bottom_collision_with(self, mat: Mat) -> bool:
        collisions = self.get_collisions_with(mat)
        m = len(self.mat[0])
        for entry in collisions:
            if entry[0] == m:
                return True
        return False

    def __str__(self) -> str:
        return '\n'.join([' '.join(str(_) for _ in row) for row in self.mat])


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move_left(self) -> 'Point':
        return Point(self.x - 1, self.y)

    def move_right(self) -> 'Point':
        return Point(self.x + 1, self.y)

    def move_down(self) -> 'Point':
        return Point(self.x, self.y + 1)


class Board:

    def __init__(self, mat: Mat=None):
        self.mat = mat if mat else Mat([])
        self.piece_size = 3
        self.arena_width  = 9
        self.arena_length = 18
        self.board_width = self.arena_width + 2
        self.board_length = self.arena_length + 1
        self._cell_empty = Int(0)
        self._cell_border = Int(1)

    def _new_row(self) -> List[Cell]:
        row: List[Cell] = []
        row.append(self._cell_border)
        for _ in range(self.arena_width):
            row.append(self._cell_empty)
        row.append(self._cell_border)
        return row

    def _new_base_row(self) -> List[Cell]:
        row: List[Cell] = []
        for _ in range(self.board_width):
            row.append(self._cell_border)
        return row

    def get_mat(self) -> Mat:
        return self.mat

    def set_mat(self, mat: Mat) -> None:
        if len(mat) != self.board_length or len(mat[0]) != self.board_width:
            assert False, 'board wrong matrix dimension: ({}, {})'.format(len(mat), len(mat) and len(mat[0]))
        self.mat = mat

    def get_matrix_at(self, pos: Point) -> Matrix:
        mat = Mat([])
        x, y = pos.x, pos.y
        for i in range(x, x + self.piece_size):
            mat.append(self.mat[i][y:y + self.piece_size])
        return Matrix(mat)

    def update_with_matrix_at(self, mat: Matrix, pos: Point) -> None:
        x, y = pos.x, pos.y
        for xi, row in enumerate(mat.get_mat()):
            for yi, col in enumerate(row):
                self.mat[x + xi][y + yi] = col

    def check_for_match_row_at(self, row: int) -> bool:
        # arena for matching rows does not include board borders.
        for col in range(1, self.board_width):
            if not self.mat[row][col].match():
                return False
        return True

    def check_for_match_row(self) -> List[int]:
        result: List[int] = []
        for irow in range(self.board_length):
            if self.check_for_match_row_at(irow):
                result.append(irow)
        return result

    def remove_rows(self, irows: List[int]) -> None:
        result = Mat([])
        result.append(self._new_base_row())
        for irow, row in enumerate(self.mat):
            if irow not in irows:
                result.append(row)
        for _ in range(self.arena_length - len(result)):
            result.append(self._new_row())
        self.set_mat(result)

    def __str__(self) -> str:
        return '\n'.join([' '.join(str(_) for _ in row) for row in self.mat])


class Piece:

    def __init__(self):
        self.matrix = None
        self.pos = None

    def move_left(self) -> Point:
        return self.pos.move_left()

    def move_right(self) -> Point:
        return self.pos.move_right()

    def move_down(self) -> Point:
        return self.pos.move_down()

    def rotate_clockwise(self) -> Matrix:
        return self.matrix.rotate_clockwise

    def rotate_anticlockwise(self) -> Matrix:
        return self.matrix.rotate_anticlockwise()


class BoardHandler:

    def __init__(self):
        self.board = None
        self.piece = None

    def _piece_move(self, new_pos: Point) -> None:
        board_mat = self.board.get_matrix_at(new_pos)
        if not self.piece.matrix.is_collision_with(board_mat):
            self.piece.pos = new_pos

    def piece_move_left(self) -> None:
        new_pos = self.piece.move_left()
        self._piece_move(new_pos)

    def piece_move_right(self) -> None:
        new_pos = self.piece.move_right()
        self._piece_move(new_pos)

    def piece_move_down(self) -> None:
        new_pos = self.piece.move_down()
        self._piece_move(new_pos)

    def _piece_rotate(self, new_mat: Matrix) -> None:
        board_mat = self.board.get_matrix_at(self.piece.pos)
        if not new_mat.is_collision_with(board_mat):
            self.piece.matrix = new_mat

    def piece_rotate_clockwise(self) -> None:
        new_mat = self.piece.rotate_clockwise()
        self._piece_rotate(new_mat)

    def piece_rotate_anticlockwise(self) -> None:
        new_mat = self.piece.rotate_anticlockwise()
        self._piece_rotate(new_mat)


if __name__ == "__main__":
    six: Mat = Mat([[Int(0), Int(0), Int(0)],
                    [Int(1), Int(1), Int(0)],
                    [Int(0), Int(1), Int(1)], ])
    mat: Matrix = Matrix(six)
    print(mat)
    for x in range(4):
        mat.set_mat(mat.rotate_clockwise().get_mat())
        print()
        print(mat)

    def _create_board(length) -> Mat:
        line: List[Cell] = [Int(1), Int(0), Int(0), Int(0), Int(0), Int(0), Int(0), Int(0), Int(0), Int(0), Int(1)]
        bottom: List[Cell] = [Int(1), Int(1), Int(1), Int(1), Int(1), Int(1), Int(1), Int(1), Int(1), Int(1), Int(1)]
        board: Mat = Mat([line[:] for x in range(length - 1)])
        board.append(bottom)
        return board

    print()
    board = Board()
    board.set_mat(_create_board(board.board_length))
    print(board)

    print()
    print(board.get_matrix_at(Point(16, 8)))

    print()
    print(mat)
    board.update_with_matrix_at(mat, Point(1, 1))
    print(board)

    while True:
        key = input('Enter: ')
        if key.lower() == 'q':
            exit(0)
