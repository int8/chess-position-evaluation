from common.transformations import Fen
from common.readers import PgnReader


def test_if_initial_position_correctly_read():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    assert positions[0]['current'].fenstring == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_if_all_positions_read():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    assert len(positions) == 82

def test_if_correct_number_of_previous_moves_kept_memory_5():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    for position in positions:
        assert len(position['prev']) == 5

def test_if_correct_number_of_previous_moves_kept_memory_0():
    positions = _load_positions_from_fischer_spassky_1972_game_6(0)
    for position in positions:
        assert len(position['prev']) == 0

def test_if_second_position_has_correct_prev_moves():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position_after_first_move = positions[1]
    for position in position_after_first_move['prev']:
        assert position.fenstring == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_if_third_position_has_correct_prev_moves():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position_after_second_move = positions[2]
    assert position_after_second_move['prev'][4].fenstring == "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1"
    for position in position_after_second_move['prev'][0:4]:
        assert position.fenstring == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_if_fourth_position_has_correct_prev_moves():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position_after_third_move = positions[3]
    assert position_after_third_move['prev'][4].fenstring == "rnbqkbnr/pppp1ppp/4p3/8/2P5/8/PP1PPPPP/RNBQKBNR w KQkq - 0 2"
    assert position_after_third_move['prev'][3].fenstring == "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1"
    for position in position_after_third_move['prev'][0:3]:
        assert position.fenstring == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_if_fifth_position_has_correct_prev_moves():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position_after_fourth_move = positions[4]
    assert position_after_fourth_move['prev'][4].fenstring == "rnbqkbnr/pppp1ppp/4p3/8/2P5/5N2/PP1PPPPP/RNBQKB1R b KQkq - 1 2"
    assert position_after_fourth_move['prev'][3].fenstring == "rnbqkbnr/pppp1ppp/4p3/8/2P5/8/PP1PPPPP/RNBQKBNR w KQkq - 0 2"
    assert position_after_fourth_move['prev'][2].fenstring == "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1"
    for position in position_after_fourth_move['prev'][0:2]:
        assert position.fenstring == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_if_position_after_15_move_is_correct():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position_after_15th_move = positions[15]
    assert position_after_15th_move['current'].fenstring == "rnbq1rk1/p1p1bpp1/1p2pn1p/3P4/3P3B/2N1PN2/PP3PPP/R2QKB1R b KQ - 0 8"
    assert position_after_15th_move['prev'][4].fenstring == "rnbq1rk1/p1p1bpp1/1p2pn1p/3p4/2PP3B/2N1PN2/PP3PPP/R2QKB1R w KQ - 0 8"
    assert position_after_15th_move['prev'][3].fenstring == "rnbq1rk1/ppp1bpp1/4pn1p/3p4/2PP3B/2N1PN2/PP3PPP/R2QKB1R b KQ - 1 7"
    assert position_after_15th_move['prev'][2].fenstring == "rnbq1rk1/ppp1bpp1/4pn1p/3p2B1/2PP4/2N1PN2/PP3PPP/R2QKB1R w KQ - 0 7"
    assert position_after_15th_move['prev'][1].fenstring == "rnbq1rk1/ppp1bppp/4pn2/3p2B1/2PP4/2N1PN2/PP3PPP/R2QKB1R b KQ - 0 6"
    assert position_after_15th_move['prev'][0].fenstring == "rnbq1rk1/ppp1bppp/4pn2/3p2B1/2PP4/2N2N2/PP2PPPP/R2QKB1R w KQ - 5 6"


def test_if_second_position_has_correct_prev_moves_after_board_flipping():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position = positions[1]
    _assert_fens_equality_of_all_positions_representation_when_flipped(position)


def test_if_10th_position_has_correct_prev_moves_after_board_flipping():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position = positions[11]
    _assert_fens_equality_of_all_positions_representation_when_flipped(position)


def test_if_18th_position_has_correct_prev_moves_after_board_flipping():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position = positions[19]
    _assert_fens_equality_of_all_positions_representation_when_flipped(position)


def test_if_13th_position_label_correctly_flipped():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position = positions[14]
    _test_if_label_is_correctly_flipped(position)


def test_if_25th_position_label_correctly_flipped():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position = positions[26]
    _test_if_label_is_correctly_flipped(position)


def test_if_65th_position_label_correctly_flipped():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position = positions[66]
    _test_if_label_is_correctly_flipped(position)


def _test_if_label_is_correctly_flipped(position):
    tensor_representation = position['current'].get_training_data(flip = True)
    if position['current'].draw():
        assert tensor_representation.result == 0
    else:
        assert tensor_representation.result ^ position['current'].result

def _load_positions_from_fischer_spassky_1972_game_6(memory_size = 0):
    positions = []
    with PgnReader("tests/test_data/FischerSpassky1972Game6.pgn", memory_size = memory_size) as reader:
        for position in iter(reader):
            positions.append(position)
    return positions

def _assert_fens_equality_of_all_positions_representation_when_flipped(position):

    f = Fen(position['current'].fenstring)
    f.flip()

    tensor_representation = position['current'].get_training_data(flip = True)
    assert tensor_representation.fenstring == f.fenstring

    for prev_positions in position['prev']:
        f = Fen(prev_positions.fenstring)
        f.flip()
        tensor_representation = prev_positions.get_training_data(flip = True)
        assert tensor_representation.fenstring == f.fenstring
