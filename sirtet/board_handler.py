from typing import Tuple, Any, cast
from sirtet.point import Point
from sirtet.cell import Cell
from sirtet.board import Board
from sirtet.matrix import Matrix
from sirtet.piece import Piece
from sirtet.shapes import Generator
from sirtet.events import Event, Events, Result_Event


class BoardHandler:
    def __init__(self):
        self.board: Board
        self.piece: Piece
        self.start_pos: Point
        self.generator: Generator

    def new_piece_at(self, pos: Point = None) -> Result_Event:
        result: Result_Event = Result_Event([])
        pos = pos if pos else self.start_pos
        self.set_new_piece_at(self.generator.get_next(), pos)
        # Check if there is any collision with the new piece.
        board_mat = self.board.get_matrix_at(pos)
        if self.piece.matrix.is_collision_with(board_mat.mat):
            result.append((Events.GAME_OVER, None))
        else:
            result.append((Events.NEW_PIECE, self.piece))
        return result

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
                return True
        return False

    def piece_move_left(self) -> None:
        new_pos = self.piece.move_left()
        self._piece_move(new_pos)

    def piece_move_right(self) -> None:
        new_pos = self.piece.move_right()
        self._piece_move(new_pos)

    def piece_move_down(self) -> Tuple[bool, Result_Event]:
        result: Result_Event = Result_Event([])
        new_pos = self.piece.move_down()
        bottomed = not self._piece_move(new_pos)
        if bottomed:
            self.board.update_with_matrix_at(self.piece.matrix, self.piece.pos)
            result.append((Events.BOTTOMED_PIECE, self.piece))
        return bottomed, result

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
        self.piece = Piece()
        self.start_pos = start_pos
        self.generator = generator
        return self

    def _process_bottomed(self) -> Result_Event:
        result: Result_Event = Result_Event([])
        matched_rows = self.board.check_for_match_row()
        if matched_rows:
            matched_cells = [
                self.board.get_arena_for_row_index(i) for i in matched_rows
            ]
            result.append((Events.MATCH_ROW, matched_cells))
            self.board.remove_rows(matched_rows)
        result.extend(self.new_piece_at())
        return result

    def _clear_for_cell(self, cell: Any) -> Result_Event:
        result: Result_Event = Result_Event([])
        self.board.clear_for_cell(cast(Cell, cell))
        return result

    def event_handler(self, event: Event, data: Any) -> Result_Event:
        bottomed: bool = False
        result: Result_Event = Result_Event([])
        if event == Events.MOVE_DOWN:
            bottomed, result = self.piece_move_down()
        elif event == Events.MOVE_LEFT:
            self.piece_move_left()
        elif event == Events.MOVE_RIGHT:
            self.piece_move_right()
        elif event == Events.ROTATE_CLOCK:
            self.piece_rotate_clockwise()
        elif event == Events.ROTATE_ANTICLOCK:
            self.piece_rotate_anticlockwise()
        elif event == Events.RENDER_ASCII:
            result = self.render_ascii(data)
        elif event == Events.CLEAR_FOR_CELL:
            result = self._clear_for_cell(data)
        if bottomed:
            result.extend(self._process_bottomed())
        return result

    def board_to_render_ascii(self) -> Board:
        b = self.board.clone()
        if self.piece.pos:
            b.update_with_matrix_at(self.piece.matrix, self.piece.pos)
        return b

    def render_ascii(self, screen: Any) -> Result_Event:
        result: Result_Event = Result_Event([])
        b = self.board_to_render_ascii()
        result.append((Events.RENDER, None))
        b.render_ascii(screen)
        return result
