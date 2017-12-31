class DataSpecs:

    tensor6x8x8_sparse = 'tensor6x8x8'
    vector6x8x8_flat = 'vector6x8x8'
    tensor12x8x8_sparse = 'tensor12x8x8'
    vector12x8x8_flat = 'vector12x8x8'

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

class Fen:

    def __init__(self, fenstring):
        self.elems = fenstring.split(" ")
        self.fenstring = fenstring

    def can_castle_white_king(self):
        return 'K' in self.elems[2]

    def can_castle_black_king(self):
        return 'k' in self.elems[2]

    def can_castle_black_queen(self):
        return 'q' in self.elems[2]

    def can_castle_white_queen(self):
        return 'Q' in self.elems[2]

    def next_to_move(self):
        return self.elems[1]

    def castling_vector(self):
        return [
            self.can_castle_black_king(),
            self.can_castle_white_king(),
            self.can_castle_black_queen(),
            self.can_castle_white_queen(),
        ]

    def en_passant_target_square(self):
        return None if self.elems[3] == '-' else self.elems[3]

    def transform(self, transformation_type = DataSpecs.vector6x8x8_flat):
        if transformation_type == DataSpecs.vector6x8x8_flat:
            return self.raw_board_to_6x8x8_flat_vector()
        elif transformation_type == DataSpecs.vector12x8x8_flat:
            return self.raw_board_to_12x8x8_flat_vector()
        elif transformation_type == DataSpecs.tensor6x8x8_sparse:
            return self.raw_board_to_6x8x8_sparse_representation()
        elif transformation_type == DataSpecs.tensor12x8x8_sparse:
            return self.raw_board_to_12x8x8_sparse_representation()
        else:
            raise ValueError("No such transformation type")

    def raw_board(self):
        return self.elems[0]

    def raw_board_to_6x8x8_flat_vector(self):
        return self._raw_board_to_flat_vector(
            DataSpecs.piece2layer_for_6x8x8_tensor, DataSpecs.piece2value_for_6x8x8_tensor, 6
        )

    def raw_board_to_12x8x8_flat_vector(self):
        return self._raw_board_to_flat_vector(
            DataSpecs.piece2layer_for_12x8x8_tensor, DataSpecs.piece2value_for_12x8x8_tensor, 12
        )

    def raw_board_to_6x8x8_sparse_representation(self):
        return self._raw_board_to_sparse_representation(
            DataSpecs.piece2layer_for_6x8x8_tensor, DataSpecs.piece2value_for_6x8x8_tensor, 6
        )

    def raw_board_to_12x8x8_sparse_representation(self):
        return self._raw_board_to_sparse_representation(
            DataSpecs.piece2layer_for_12x8x8_tensor, DataSpecs.piece2value_for_12x8x8_tensor, 12
        )

    def flip_position(self):
        self.elems[0] = "".join(reversed([self._reverse_piece(piece) for piece in self.elems[0]]))

    def flip_castling(self):
        tmp_color_changed = [self._reverse_piece(piece) for piece in self.elems[2]]
        self.elems[2] = "".join(sorted(tmp_color_changed))

    def flip(self):
        self.elems[1] = 'w' if self.next_to_move() == 'b' else 'b'
        self.flip_position()
        self.flip_castling()
        self.fenstring = " ".join(self.elems)


    def _reverse_piece(self, piece):
        if piece.islower():
            return piece.upper()
        if piece.isupper():
            return piece.lower()
        return piece

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

    def _raw_board_to_flat_vector(self, piece_to_layer_map, piece_to_value_map, layers):
        raw_board = self.raw_board()
        row = 0; column = 0
        vector = [0 for _ in range(0, 8*8*layers)]
        for c in raw_board:
            if c.isdigit():
                column = column + int(c)
            elif c == '/':
                row = row + 1
                column = 0
            else:
                vector[layers*(8*row + column) + piece_to_layer_map[c]] = piece_to_value_map[c]
                column = column + 1
        return vector
