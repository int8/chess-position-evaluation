from common.chessposition import ChessGame
import chess

class PgnReader:

    def __init__(self, pgn_file, memory_size = 0):
        self.memory_size = memory_size
        self.pgn = open(pgn_file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        close(self.pgn)

    def __iter__(self):
        self.current_game = ChessGame(chess.pgn.read_game(self.pgn))
        while self.current_game:
            self.current_game.play_main_line()
            self.current_game.extract_result()
            positions = self.current_game.generate_game_positions(self.memory_size)
            for position in positions:
                yield position
            self.current_game = ChessGame(chess.pgn.read_game(self.pgn))
