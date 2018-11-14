from typing import NewType
from sirtet.point import Point
from sirtet.board import Board
from sirtet.matrix import Matrix
from sirtet.piece import Piece
from sirtet.shapes import Generator
from sirtet.logic import Logic


BH_Event = NewType("BH_Event", int)


class BoardHandler:

    MOVE_DOWN = BH_Event(1)
    MOVE_LEFT = BH_Event(2)
    MOVE_RIGHT = BH_Event(3)
    ROTATE_CLOCK = BH_Event(4)
    ROTATE_ANTICLOCK = BH_Event(5)

    def __init__(self):
        self.board: Board
        self.piece: Piece
        self.start_pos: Point
        self.generator: Generator
        self.logic: Logic

    def new_piece_at(self, pos: Point = None) -> None:
        pos = pos if pos else self.start_pos
        self.set_new_piece_at(self.generator.get_next(), pos)
        # Check if there is any collision with the new piece.
        board_mat = self.board.get_matrix_at(pos)
        if self.piece.matrix.is_collision_with(board_mat.mat):
            self.logic.event_handler(Logic.GAME_OVER, None)
        self.logic.event_handler(Logic.NEW_PIECE, self.piece)

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
            self.logic.event_handler(Logic.BOTTOMED_PIECE, self.piece)
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
        self, board: Board, generator: Generator, logic: Logic, start_pos: Point
    ) -> "BoardHandler":
        self.board = board
        self.piece = Piece()
        self.start_pos = start_pos
        self.generator = generator
        self.logic = logic
        return self

    def _process_bottomed(self) -> None:
        matched_rows = self.board.check_for_match_row()
        if matched_rows:
            matched_cells = [
                self.board.get_arena_for_row_index(i) for i in matched_rows
            ]
            self.logic.event_handler(Logic.MATCH_ROW, matched_cells)
            self.board.remove_rows(matched_rows)
        self.new_piece_at()

    def event_handler(self, event: BH_Event) -> bool:
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
            self._process_bottomed()
        return bottomed

    def board_to_render(self) -> Board:
        b = self.board.clone()
        if self.piece.pos:
            b.update_with_matrix_at(self.piece.matrix, self.piece.pos)
        return b

    def render(self) -> None:
        b = self.board_to_render()
        self.logic.event_handler(Logic.RENDER, None)
        b.render()
