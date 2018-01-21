from common.transformations import Fen, DataSpecs
from common.io import PgnReader


def test_if_position_length_is_8x8x6():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    vector = positions[0]['current'].get_training_data(transformation_type = DataSpecs.vector6x8x8_flat)
    assert len(vector.board_data) == 6*8*8

def test_if_initial_position_non_zero_values_is_32_for_flat_vector_6x8x8():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    vector = positions[0]['current'].get_training_data(transformation_type = DataSpecs.vector6x8x8_flat)
    assert len([1 for p in vector.board_data if p != 0]) == 32


def test_if_initial_position_white_and_black_pieces_number_is_16_for_flat_vector_6x8x8():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    vector = positions[0]['current'].get_training_data(transformation_type = DataSpecs.vector6x8x8_flat)
    assert len([1 for p in vector.board_data if p > 0]) == 16
    assert len([1 for p in vector.board_data if p < 0]) == 16

def test_if_position_length_is_12x8x8():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    vector = positions[0]['current'].get_training_data(transformation_type = DataSpecs.vector12x8x8_flat)
    assert len(vector.board_data) == 12*8*8

def test_if_initial_position_non_zero_values_is_32_for_flat_vector_12x8x8():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    vector = positions[0]['current'].get_training_data(transformation_type = DataSpecs.vector12x8x8_flat)
    assert len([1 for p in vector.board_data if p != 0]) == 32

def test_if_castling_vector_length_is_4():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    vector = positions[0]['current'].get_training_data(transformation_type = DataSpecs.vector6x8x8_flat)
    assert len(vector.castlings_vector) == 4

def test_if_initial_castling_vector_is_correct():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    vector = positions[0]['current'].get_training_data(transformation_type = DataSpecs.vector6x8x8_flat)
    assert vector.castlings_vector == [1,1,1,1]


def test_if_initial_position_vector_is_correct_for_6x8x8():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    vector = positions[0]['current'].get_training_data(transformation_type = DataSpecs.vector6x8x8_flat)
    for i in range(0, 16*6, 6):
        non_zero_elems = list(filter(lambda x : x != 0, vector.board_data[i:(i+6)]))
        assert non_zero_elems == [1]

    for i in range(16*6, 48*6, 6):
        non_zero_elems = list(filter(lambda x : x != 0, vector.board_data[i:(i+6)]))
        assert len(non_zero_elems) == 0

    for i in range(48*6, 64*6, 6):
        non_zero_elems = list(filter(lambda x : x != 0, vector.board_data[i:(i+6)]))
        assert non_zero_elems == [-1]


def test_if_initial_position_vector_is_correct_for_12x8x8():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    vector = positions[0]['current'].get_training_data(transformation_type = DataSpecs.vector12x8x8_flat)
    for i in range(0, 16*12, 12):
        non_zero_elems = list(filter(lambda x : x != 0, vector.board_data[i:(i+12)]))
        assert non_zero_elems == [1]

    for i in range(16*12, 48*12, 12):
        non_zero_elems = list(filter(lambda x : x != 0, vector.board_data[i:(i+12)]))
        assert len(non_zero_elems) == 0

    for i in range(48*12, 64*12, 12):
        non_zero_elems = list(filter(lambda x : x != 0, vector.board_data[i:(i+12)]))
        assert non_zero_elems == [1]

def _load_positions_from_fischer_spassky_1972_game_6(memory_size = 0):
    positions = []
    with PgnReader("tests/test_data/FischerSpassky1972Game6.pgn", memory_size = memory_size) as reader:
        for position in iter(reader):
            positions.append(position)
    return positions
