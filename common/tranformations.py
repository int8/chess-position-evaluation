from chessposition import TensorPositionWithContext

class TensorSpec:

    piece2layer_for_6x8x8_tensor = {
        'p': 0,'P': 0,'n': 1,'N': 1,'b': 2,'B': 2,
        'r': 3,'R': 3,'q': 4,'Q': 4,'k': 5,'K': 5
    }

    piece2value_for_6x8x8_tensor = {
        'p': 1,'P': -1,'n': 1,'N': -1,'b': 1,'B': -1,
        'r': 1,'R': -1,'q': 1,'Q': -1,'k': 1,'K': -1
    }

    piece2layer_for_12x8x8_tensor = {
        'p': 0,'P': 1,'n': 2,'N': 3,'b': 4,'B': 5,
        'r': 6,'R': 7,'q': 8,'Q': 9,'k': 10,'K': 11
    }

    piece2value_for_12x8x8_tensor = {
        'p': 1,'P': 1,'n': 1,'N': 1,'b': 1,'B': 1,
        'r': 1,'R': 1,'q': 1,'Q': 1,'k': 1,'K': 1
    }

class FenTranformation:

    def __init__(self, fen):
        self.elems = fen.split(" ")

    def can_castle_white_king(self):
        return 'K' in self.elems[2]

    def can_castle_black_king(self):
        return 'k' in self.elems[2]

    def can_castle_black_queen(self):
        return 'q' in self.elems[2]

    def can_castle_white_queen(self):
        return 'Q' in self.elems[2]

    def castling_vector(self):
        return [
            self.can_castle_black_king(),
            self.can_castle_white_king(),
            self.can_castle_black_queen(),
            self.can_castle_white_queen(),
        ]


    def en_passant_target_square(self):
        return None if self.elems[3] == '-' else self.elems[3]

    def raw_board(self):
        return self.elems[0]

    def _raw_board_to_sparse_representation(self, piece_to_layer_map, piece_to_value_map, layers):
        raw_board = self.raw_board()
        row = 0; column = 0
        indices_x = []
        indices_y = []
        indices_z = []
        values = []
        for c in raw_board:
            if c.isdigit():
                column = column + int(c)
            elif c == '/':
                row = row + 1
                column = 0
            else:
                indices_z.append(piece_to_layer_map[c])
                indices_x.append(row)
                indices_y.append(column)
                values.append(piece_to_value_map[c])
                column = column + 1

        return ({'indices_z': indices_z, 'indices_x': indices_x, 'indices_y': indices_y, 'values': values})

    def raw_board_to_6x8x8_sparse_representation(self):
        return self._raw_board_to_sparse_representation(
            TensorSpec.piece2layer_for_6x8x8_tensor, TensorSpec.piece2value_for_6x8x8_tensor, 6
        )

    def raw_board_to_12x8x8_sparse_representation(self):
        return self._raw_board_to_sparse_representation(
            TensorSpec.piece2layer_for_12x8x8_tensor, TensorSpec.piece2value_for_12x8x8_tensor, 12
        )


class Position2SparseRepresentation:

    def transform_position_with_context(self, position):
        f = FenTranformation(position.position)
        tensor_position = TensorPositionWithContext(
            current_position = f.raw_board_to_6x8x8_sparse_representation(),
            castlings_data = f.castling_vector(),
            number_of_moves = position.number_of_moves,
            fen = position.position
        )

        prev_positions = []
        for i in xrange(len(position.context)):
            f_prev = FenTranformation(position.context[i].position)
            prev_positions.append(
                TensorPositionWithContext(
                    current_position = f_prev.raw_board_to_6x8x8_sparse_representation(),
                    castlings_data = f_prev.castling_vector(),
                    number_of_moves = position.context[i].number_of_moves,
                    fen = position.context[i].position
                )
            )

        return {
            'current_position': tensor_position,
            'prev_positions': prev_positions,
            'winner': position.result,
            'ends_with_checkmate': position.checkmate
        }
