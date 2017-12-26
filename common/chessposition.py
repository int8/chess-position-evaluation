import chess.pgn

class TensorPositionWithContext:

    def __init__(self, current_position, castlings_data, number_of_moves, fen):
        self.current_position = current_position
        self.castlings_data = castlings_data
        self.number_of_moves = number_of_moves
        self.fen = fen

class PositionWithContext:

    def __init__(self, position, context, number_of_moves, checkmate, result):
        self.position = position
        self.context = context
        self.number_of_moves = number_of_moves
        self.checkmate = checkmate
        self.result = result

    def white_wins(self):
        return self.result == 1

    def black_wins(self):
        return self.result == 0

    def draw(self):
        return self.result == -1

    def __str__(self):
        return str({
            'position':  self.position,
            'context': self.context,
            'number_of_moves': self.number_of_moves,
            'checkmate': self.checkmate,
            'result': self.result
        })

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
            context = []
            for j in range(1 , memory_size + 1):
                if i - j < 0:
                    context.append(PositionWithContext(self.game_positions[0], [], None, False, self.result))
                else:
                    context.append(PositionWithContext(self.game_positions[i-j], [], None, False, self.result))
            positions.append(
                PositionWithContext(
                    position = self.game_positions[i],
                    context = context[::-1],
                    number_of_moves = self.number_of_moves,
                    checkmate = self.checkmate,
                    result = self.result
                )
            )
        return positions
