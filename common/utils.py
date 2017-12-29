class TensorPositionVizualizer:

    def __init__(self, position):
        self.position = position

    def get_text_board(self, btype = '6x8x8'):
        zipped_coordinates = zip(
            self.position.current_position['indices_x'],
            self.position.current_position['indices_y'],
            self.position.current_position['indices_z'],
            self.position.current_position['values']
        )
        if btype == '6x8x8':
            board = self.get_board_6x8x8(zipped_coordinates)
        else:
            raise NotImplemented()
        return board

    def get_board_6x8x8(self, zipped_coordinates):
        v = [['_' for _ in xrange(8)] for _ in xrange(8)]
        for coords in zipped_coordinates:
            if coords[2] == 0:
                val = 'p'
            if coords[2] == 1:
                val = 'n'
            if coords[2] == 2:
                val = 'b'
            if coords[2] == 3:
                val = 'r'
            if coords[2] == 4:
                val = 'q'
            if coords[2] == 5:
                val = 'k'
            if coords[3] < 0:
                val = val.upper()
            if coords[3] > 0:
                val = val.lower()
            v[coords[0]][coords[1]] = val
        return v
