import torch
import uuid
from random import shuffle
import gzip


def reverse_piece(piece):
    if piece.islower():
        return piece.upper()
    if piece.isupper():
        return piece.lower()
    return piece

class DataSaverWithShuffling:
    def __init__(self,output_dir, chunk_size, number_of_buckets = 50):
        self.output_dir = output_dir
        self.chunk_size = chunk_size
        self.number_of_buckets = number_of_buckets
        self.chunks = [list([]) for _ in range(0,number_of_buckets)]
        self.current_order_of_inserting = range(0,self.number_of_buckets)[::-1]
        shuffle(self.current_order_of_inserting)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for chunk in self.chunks:
            if len(chunk) > 0:
                with gzip.open(self.output_dir + '/' + str(uuid.uuid1()) + '.pt' , 'wb') as f:
                    torch.save(chunk, f)

    def insert_next(self, obj):

        if len(self.current_order_of_inserting) == 0:
            self.current_order_of_inserting = range(0,self.number_of_buckets)
            shuffle(self.current_order_of_inserting)

        current_chunk = self.current_order_of_inserting.pop()
        self.chunks[current_chunk].append(obj)
        if len(self.chunks[current_chunk]) > self.chunk_size:
            with gzip.open(self.output_dir + '/' + str(uuid.uuid1()) + '.pt' , 'wb') as f:
                torch.save(self.chunks[current_chunk], f)
            self.chunks[current_chunk] = []

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
