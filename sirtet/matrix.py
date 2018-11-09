from typing import List, Tuple, Any, NewType


class Cell:

    def __init__(self, content: Any):
        self._content = content

    def collision(self, other: 'Cell') -> bool:
        pass

    def match(self) -> bool:
        pass

    def update_with(self, other: 'Cell') -> None:
        self._content = other._content

    def clone(self) -> 'Cell':
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

    def update_with(self, other: 'Cell') -> None:
        if self._content == 0:
            self._content = other._content

    def clone(self) -> 'Cell':
        return Int(self._content)

    def __str__(self) -> str:
        if self._content == 0:
            return ' '
        # return str(self._content)
        return chr(9608)


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
        return len(self.get_collisions_with(mat)) != 0

    def is_bottom_collision_with(self, mat: Mat) -> bool:
        collisions = self.get_collisions_with(mat)
        m = len(self.mat)
        for entry in collisions:
            if entry[0] == (m - 1):
                return True
        return False

    def __str__(self) -> str:
        return '\n'.join([' '.join(str(_) for _ in row) for row in self.mat])


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move_left(self) -> 'Point':
        return Point(self.x, self.y - 1)

    def move_right(self) -> 'Point':
        return Point(self.x, self.y + 1)

    def move_down(self) -> 'Point':
        return Point(self.x + 1, self.y)


class Board:

    def __init__(self, mat: Mat=None):
        self.mat = mat if mat else Mat([])
        self.piece_size = 3
        self.arena_width  = 9
        self.arena_height = 18
        self.board_width = self.arena_width + 2
        self.board_height = self.arena_height + 1

    def new_cell_empty(self) -> Cell:
        return Int(0)

    def new_cell_border(self) -> Cell:
        return Int(1)

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

    def new_clean_mat(self) -> Mat:
        mat = Mat([])
        for _ in range(self.board_height - 1):
            mat.append(self._new_row())
        mat.append(self._new_bottom_row())
        return mat

    def clone(self) -> 'Board':
        b = Board()
        for x in range(self.board_height):
            b.mat.append([])
            for y in range(self.board_width):
                b.mat[x].append(self.mat[x][y].clone())
        return b

    def get_mat(self) -> Mat:
        return self.mat

    def set_mat(self, mat: Mat) -> None:
        if len(mat) != self.board_height or len(mat[0]) != self.board_width:
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
                # self.mat[x + xi][y + yi] = col
                self.mat[x + xi][y + yi].update_with(col)

    def clear_with_matrix_at(self, mat: Matrix, pos: Point) -> None:
        x, y = pos.x, pos.y
        for xi, row in enumerate(mat.get_mat()):
            for yi, col in enumerate(row):
                self.mat[x + xi][y + yi] = self.new_cell_empty()

    def check_for_match_row_at(self, row: int) -> bool:
        # arena for matching rows does not include board borders.
        for col in range(1, self.board_width):
            if not self.mat[row][col].match():
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
        return '\n'.join([' '.join(str(_) for _ in row) for row in self.mat])


BH_Event = NewType('BH_Event', int)


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
        return self.matrix.rotate_clockwise()

    def rotate_anticlockwise(self) -> Matrix:
        return self.matrix.rotate_anticlockwise()


class BoardHandler:

    MOVE_DOWN = BH_Event(1)
    MOVE_LEFT = BH_Event(2)
    MOVE_RIGHT = BH_Event(3)
    ROTATE_CLOCK = BH_Event(4)
    ROTATE_ANTICLOCK = BH_Event(5)

    def __init__(self):
        self.board = None
        self.piece = None
        self.start_pos: Point
        self.mats: List[Mat]
        self.__mat_index: int = 0

    def new_piece_at(self, pos: Point=None) -> None:
        self.set_new_piece_at(Matrix(self.mats[self.__mat_index]))
        self.__mat_index = (self.__mat_index + 1) % len(self.mats)

    def set_new_piece_at(self, mat: Matrix, pos: Point=None) -> None:
        self.piece.matrix = mat
        self.piece.pos = pos if pos else self.start_pos

    def _check_pos(self, new_pos: Point) -> bool:
        x, y = new_pos.x, new_pos.y
        x_boundary = self.board.board_height - self.board.piece_size
        y_boundary = self.board.board_width - self.board.piece_size
        return (0 <= x <= x_boundary) and (0 <= y <= y_boundary)

    def _piece_move(self, new_pos: Point) -> bool:
        if self._check_pos(new_pos):
            board_mat = self.board.get_matrix_at(new_pos)
            if not self.piece.matrix.is_collision_with(board_mat.mat):
                self.piece.pos = new_pos
                return False
        return True

    def piece_move_left(self) -> None:
        new_pos = self.piece.move_left()
        self._piece_move(new_pos)

    def piece_move_right(self) -> None:
        new_pos = self.piece.move_right()
        self._piece_move(new_pos)

    def piece_move_down(self) -> bool:
        new_pos = self.piece.move_down()
        bottomed = self._piece_move(new_pos)
        if bottomed:
            self.board.update_with_matrix_at(self.piece.matrix, self.piece.pos)
        return bottomed

    def _piece_rotate(self, new_mat: Matrix) -> None:
        board_mat = self.board.get_matrix_at(self.piece.pos)
        if not new_mat.is_collision_with(board_mat.mat):
            self.piece.matrix = new_mat

    def piece_rotate_clockwise(self) -> None:
        new_mat = self.piece.rotate_clockwise()
        self._piece_rotate(new_mat)

    def piece_rotate_anticlockwise(self) -> None:
        new_mat = self.piece.rotate_anticlockwise()
        self._piece_rotate(new_mat)

    def setup(self, mats: List[Mat], start_pos: Point) -> 'BoardHandler':
        self.board = Board()
        self.board.set_mat(self.board.new_clean_mat())
        self.piece = Piece()
        self.start_pos = start_pos
        self.mats = mats
        return self

    def event_handler(self, event: BH_Event):
        bottomed: bool = False
        if event == BoardHandler.MOVE_DOWN:
            bottomed = self.piece_move_down()
        elif event == BoardHandler.MOVE_LEFT:
            self.piece_move_left()
            bottomed = self.piece_move_down()
        elif event == BoardHandler.MOVE_RIGHT:
            self.piece_move_right()
            bottomed = self.piece_move_down()
        elif event == BoardHandler.ROTATE_CLOCK:
            self.piece_rotate_clockwise()
            bottomed = self.piece_move_down()
        elif event == BoardHandler.ROTATE_ANTICLOCK:
            self.piece_rotate_anticlockwise()
            bottomed = self.piece_move_down()
        if bottomed:
            matched_rows = self.board.check_for_match_row()
            if matched_rows:
                self.board.remove_rows(matched_rows)
            self.new_piece_at()
        return bottomed

    def render_to(self) -> Board:
        b = self.board.clone()
        if self.piece.pos:
            b.update_with_matrix_at(self.piece.matrix, self.piece.pos)
        return b


if __name__ == "__main__":
    mats: List[Mat] = [Mat([[Int(0), Int(0), Int(0)],
                            [Int(1), Int(1), Int(0)],
                            [Int(0), Int(1), Int(1)], ]),
                       Mat([[Int(0), Int(0), Int(0)],
                            [Int(0), Int(1), Int(1)],
                            [Int(1), Int(1), Int(0)], ]),
                       Mat([[Int(1), Int(0), Int(0)],
                            [Int(1), Int(0), Int(0)],
                            [Int(1), Int(1), Int(0)], ]),
                       Mat([[Int(0), Int(0), Int(1)],
                            [Int(0), Int(0), Int(1)],
                            [Int(0), Int(1), Int(1)], ]),
                       Mat([[Int(0), Int(1), Int(0)],
                            [Int(0), Int(1), Int(0)],
                            [Int(0), Int(1), Int(0)], ]), ]

    bh: BoardHandler = BoardHandler()
    bh.setup(mats, Point(0, 1))
    bh.new_piece_at()
    while True:
        print()
        print(bh.render_to())
        key = input('Enter: ').lower()
        if key == 'x':
            exit(0)
        elif key == '':
            bh.event_handler(BoardHandler.MOVE_DOWN)
        elif key == 'a':
            bh.event_handler(BoardHandler.MOVE_LEFT)
        elif key == 's':
            bh.event_handler(BoardHandler.MOVE_RIGHT)
        elif key == 'q':
            bh.event_handler(BoardHandler.ROTATE_ANTICLOCK)
        elif key == 'w':
            bh.event_handler(BoardHandler.ROTATE_CLOCK)
