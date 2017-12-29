from common.chessposition import ChessGame
import chess
import os
from random import sample, shuffle
import torch
import gzip
import uuid

class PgnReader:

    def __init__(self, pgn_file, memory_size = 0):
        self.memory_size = memory_size
        self.pgn = open(pgn_file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pgn.close()

    def __iter__(self):
        self.current_game = ChessGame(chess.pgn.read_game(self.pgn))
        while self.current_game:
            self.current_game.play_main_line()
            self.current_game.extract_result()
            positions = self.current_game.generate_game_positions(self.memory_size)
            for position in positions:
                yield position
            self.current_game = ChessGame(chess.pgn.read_game(self.pgn))

class PositionReader:

    def append_new_data(self, new_data):
        raise NotImplemented()

    def is_load_needed(self):
        raise NotImplemented()

    def get_next_batch(self):
        raise NotImplemented()

    def __init__(self, data_directory, number_of_files_in_memory = 100, batch_size = 100):
        self.number_of_files_in_memory = number_of_files_in_memory
        self.data_directory = data_directory
        self.files = os.listdir(data_directory)
        if len(self.files) == 0:
            raise ValueError("directory contains no files")

        self.files_shuffled = sample(self.files, len(self.files))
        self.data = None
        self.batch_size = batch_size
        self.current_index = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __iter__(self):
        while True:
            if self.is_load_needed():
                self.current_index = 0
                self.data = None
                self.load_next_data_portion()
            yield self.get_next_batch()

    def get_number_of_observations(self):
        return self.data['X'].shape[0] if self.data else 0

    def get_next_file_name(self):
        if len(self.files_shuffled) > 0:
            return self.files_shuffled.pop()
        self.files_shuffled = sample(self.files, len(self.files))
        return self.get_next_file_name()

    def load_next_data_portion(self):
        for i in range(0, self.number_of_files_in_memory):
            filename = self.get_next_file_name()
            with gzip.open(self.data_directory + '/' + filename, 'rb') as f:
                data = torch.load(f)
                print filename
            self.append_new_data(data)


class TensorPositionReader(PositionReader):
    def append_new_data(self, new_data):
        ind_x = []; ind_z = []; ind_y = []; value = [];
        data = {'X': torch.CharTensor(len(new_data), 6,8,8), 'Y': [0] * len(new_data)}

        for i in range(0, len(new_data)):
            ind_x = new_data[i]['current'].board_tensor['indices_x']
            ind_y = new_data[i]['current'].board_tensor['indices_y']
            ind_z = new_data[i]['current'].board_tensor['indices_z']
            value = new_data[i]['current'].board_tensor['values']
            data['X'][[i for _ in value], ind_z, ind_x, ind_y] = torch.CharTensor(value)
            data['Y'][i] = new_data[i]['current'].result

        if not self.data:
            self.data = data
        else:
            self.data['X'] = torch.cat((self.data['X'], data['X']), 0)
        self.data['Y'] = self.data['Y'] + data['Y']

    def is_load_needed(self):
        return (self.data == None) or (self.current_index + self.batch_size > self.get_number_of_observations())

    def get_next_batch(self):
        self.current_index += self.batch_size
        return {
            'X': self.data['X'][self.current_index:(self.current_index + self.batch_size),:,:,:],
            'Y': self.data['Y'][self.current_index:(self.current_index + self.batch_size)]
        }


class FileSystemDataSaverWithShuffling:

    def __init__(self, output_dir, chunk_size = 5000, number_of_buckets = 50):
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
