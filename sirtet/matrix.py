from typing import List, Tuple, Any, NewType


class Cell:

    def __init__(self, content: Any):
        self._content = content

    def collision(self, other: Any) -> bool:
        pass

    def __str__(self) -> str:
        pass


class Int(Cell):

    def __init__(self, content: Any):
        super(Int, self).__init__(content)

    def collision(self, other: 'Int') -> bool:
        return self._content != 0 and other ._content != 0

    def __str__(self) -> str:
        return str(self._content)


# Mat = NewType('Mat', List[List[Cell]])


class Matrix:

    def __init__(self, m: List[List[Cell]]):
        self.matrix: List[List[Cell]] = []
        self.set(m)

    def _check(self, m: List[List[Cell]]) -> bool:
        if m is None or len(m) != 3 or len(m[0]) != 3:
            return False
        return True

    def get(self) -> List[List[Cell]]:
        return self.matrix

    def set(self, m) -> None:
        if not self._check(m):
            assert False, 'wrong matrix dimension: {}'.format(m)
        self.matrix = m[:]

    def rotate_clockwise(self) -> 'Matrix':
        """Rotate nxn matrix by 90 degrees clockwise.
        """
        #result matrix
        result = [row[:] for row in self.matrix]
        m = len(self.matrix[0])
        for x in range(0, m):
            for j in range(0, m):
                result[j][m - 1 - x] = self.matrix[x][j]
        return Matrix(result)

    def rotate_anticlockwise(self) -> 'Matrix':
        """Rotate nxn matrix by 90 degrees anti-clockwise.
        """
        #result matrix
        result = [row[:] for row in self.matrix]
        m = len(self.matrix[0])
        for x in range(0, m):
            for j in range(0, m):
                result[x][j] = self.matrix[j][m - 1 - x]
        return Matrix(result)

    def get_collisions_with(self, mat: List[List[Cell]]) -> List[Tuple]:
        if not self._check(mat):
            assert False, 'wrong matrix dimension: {}'.format(mat)
        m = len(self.matrix[0])
        collisions: List[Tuple] = []
        for x in range(m):
            for y in range(m):
                if self.matrix[x][y].collision(mat[x][y]):
                    collisions.append((x, y))
        return collisions

    def is_collision_with(self, mat: List[List[Cell]]) -> bool:
        return self.get_collisions_with(mat) != 0

    def is_bottom_collision_with(self, mat: List[List[Cell]]) -> bool:
        collisions = self.get_collisions_with(mat)
        m = len(self.matrix[0])
        for entry in collisions:
            if entry[0] == m:
                return True
        return False

    def __str__(self) -> str:
        return '\n'.join([' '.join(str(_) for _ in row) for row in self.matrix])


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

    def __init__(self, board: List[List[Cell]]=None):
        self.board = self._create_board()
        self.piece_size = 3

    def _create_board(self) -> List[List[Cell]]:
        line: List[Cell] = [Int(1), Int(0), Int(0), Int(0), Int(0), Int(0), Int(0), Int(0), Int(0), Int(0), Int(1)]
        bottom: List[Cell] = [Int(1), Int(1), Int(1), Int(1), Int(1), Int(1), Int(1), Int(1), Int(1), Int(1), Int(1)]
        board: List[List[Cell]] = [line for x in range(18)]
        board.append(bottom)
        return board

    def get_matrix_at(self, pos: Point) -> Matrix:
        mat = []
        x, y = pos.x, pos.y
        for i in range(x, x + self.piece_size):
            mat.append(self.board[i][y:y + self.piece_size])
        return Matrix(mat)

    def __str__(self) -> str:
        return '\n'.join([' '.join(str(_) for _ in row) for row in self.board])


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
    six: List[List[Cell]] = [[Int(0), Int(0), Int(0)],
                             [Int(1), Int(1), Int(0)],
                             [Int(0), Int(1), Int(1)], ]
    mat: Matrix = Matrix(six)
    print(mat)
    for x in range(4):
        mat.set(mat.rotate_clockwise())
        print()
        print(mat)

    print()
    board = Board()
    print(board)

    print()
    print(board.get_matrix_at(Point(16, 8)))
