from typing import NewType
from sirtet.point import Point
from sirtet.board import Board
from sirtet.matrix import Matrix
from sirtet.piece import Piece
from sirtet.shapes import Generator


BH_Event = NewType("BH_Event", int)


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
        self.generator: Generator

    def new_piece_at(self, pos: Point = None) -> None:
        pos = pos if pos else self.start_pos
        self.set_new_piece_at(self.generator.get_next(), pos)
        # Check if there is any collision with the new piece.
        board_mat = self.board.get_matrix_at(pos)
        if self.piece.matrix.is_collision_with(board_mat.mat):
            print("GAME OVER")
            exit(0)

    def set_new_piece_at(self, mat: Matrix, pos: Point) -> None:
        self.piece.matrix = mat
        self.piece.pos = pos

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

    def setup(
        self, board: Board, generator: Generator, start_pos: Point
    ) -> "BoardHandler":
        self.board = board
        # TODO: This could be moved outside to the module where Board is
        # created.
        self.board.set_mat(self.board.new_clean_mat())
        self.piece = Piece()
        self.start_pos = start_pos
        self.generator = generator
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
