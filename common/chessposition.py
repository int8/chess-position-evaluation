import chess.pgn
from common.transformations import Fen
from common.transformations import DataSpecs

class ChessPositionVectorRepresentation:

    def __init__(self, board_data, castlings_vector, next_to_move, game_final_length, fenstring, result, transformation_type):
        self.board_data = board_data
        self.castlings_vector = castlings_vector
        self.next_to_move = next_to_move
        self.game_final_length = game_final_length
        self.fenstring = fenstring
        self.result = result
        self.transformation_type = transformation_type

class Position:

    def __init__(self, fenstring, game_final_length, checkmate, result):
        self.fen = Fen(fenstring)
        self.game_final_length = game_final_length
        self.checkmate = checkmate
        self.result = result

    def white_wins(self):
        return self.result == 1

    def black_wins(self):
        return self.result == 0

    def draw(self):
        return self.result == -1

    def get_training_data(self, transformation_type = DataSpecs.vector12x8x8_flat, flip = True):
        if flip:
            self.fen.flip()

        result = None if self.draw() else (self.white_wins() ^ flip)

        return ChessPositionVectorRepresentation(
            board_data = self.fen.transform(transformation_type),
            castlings_vector = self.fen.castling_vector(),
            game_final_length = self.game_final_length,
            next_to_move = self.fen.next_to_move(),
            fenstring = self.fen.fenstring,
            result = result,
            transformation_type = transformation_type
        )

    @property
    def fenstring(self):
        return self.fen.fenstring

    @property
    def white_to_move(self):
        return self.fen.next_to_move() == 'w'

    @property
    def black_to_move(self):
        return self.fen.next_to_move() == 'b'


class ChessGame:

    def __bool__(self):
        return True if self.current_game else False
    __nonzero__ = __bool__

    def __init__(self, initial_game_state):
        self.current_game = initial_game_state

    def extract_result(self):
        if self.current_game.headers["Result"] == "1-0":
            self.result = 1
        elif self.current_game.headers["Result"] == "0-1":
            self.result = 0
        else:
            self.result = -1

    def draw(self):
        return self.result == -1

    def play_main_line(self):
        self.current_board = self.current_game.board()
        self.game_positions = [self.current_board.fen()]
        for move in self.current_game.main_line():
            self.current_board.push(move)
            self.game_positions.append(self.current_board.fen())

        self.checkmate = self.current_board.is_checkmate()
        self.number_of_moves =  len(self.game_positions) / 2 + 1

    def generate_game_positions(self, memory_size = 1):
        positions = []
        for i in range(0, len(self.game_positions)):
            positions.append(
                {   'current': Position(
                        fenstring = self.game_positions[i],
                        game_final_length = self.number_of_moves,
                        checkmate = self.checkmate,
                        result = self.result
                    ),
                    'prev': self._generate_prev_positions(memory_size , current_position_index = i)
                }
            )
        return positions


    def _generate_prev_positions(self, prev_positions_to_keep, current_position_index):
        prev_positions = []
        for j in range(1 , prev_positions_to_keep + 1):
            if current_position_index - j < 0:
                prev_positions.append(Position(self.game_positions[0], self.number_of_moves, self.checkmate, self.result))
            else:
                prev_positions.append(Position(self.game_positions[current_position_index-j], self.number_of_moves, self.checkmate, self.result))
        return prev_positions[::-1]
