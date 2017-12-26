from common.transformations import FenTranformation, Position2SparseRepresentation
from common.readers import PgnReader

def test_if_initial_position_correctly_read():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    assert positions[0].position == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_if_all_positions_read():
    positions = _load_positions_from_fischer_spassky_1972_game_6()
    assert len(positions) == 82

def test_if_correct_number_of_previous_moves_kept():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    for position in positions:
        assert len(position.context) == 5

def test_if_second_position_has_correct_prev_moves():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position_after_first_move = positions[1]
    for position in position_after_first_move.context:
        assert position.position == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_if_third_position_has_correct_prev_moves():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position_after_second_move = positions[2]
    assert position_after_second_move.context[4].position == "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1"
    for position in position_after_second_move.context[0:4]:
        assert position.position == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_if_fourth_position_has_correct_prev_moves():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position_after_third_move = positions[3]
    assert position_after_third_move.context[4].position == "rnbqkbnr/pppp1ppp/4p3/8/2P5/8/PP1PPPPP/RNBQKBNR w KQkq - 0 2"
    assert position_after_third_move.context[3].position == "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1"
    for position in position_after_third_move.context[0:3]:
        assert position.position == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_if_fifth_position_has_correct_prev_moves():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position_after_fourth_move = positions[4]
    assert position_after_fourth_move.context[4].position == "rnbqkbnr/pppp1ppp/4p3/8/2P5/5N2/PP1PPPPP/RNBQKB1R b KQkq - 1 2"
    assert position_after_fourth_move.context[3].position == "rnbqkbnr/pppp1ppp/4p3/8/2P5/8/PP1PPPPP/RNBQKBNR w KQkq - 0 2"
    assert position_after_fourth_move.context[2].position == "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1"
    for position in position_after_fourth_move.context[0:2]:
        assert position.position == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_if_position_after_15_move_is_correct():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position_after_15th_move = positions[15]
    assert position_after_15th_move.position == "rnbq1rk1/p1p1bpp1/1p2pn1p/3P4/3P3B/2N1PN2/PP3PPP/R2QKB1R b KQ - 0 8"
    assert position_after_15th_move.context[4].position == "rnbq1rk1/p1p1bpp1/1p2pn1p/3p4/2PP3B/2N1PN2/PP3PPP/R2QKB1R w KQ - 0 8"
    assert position_after_15th_move.context[3].position == "rnbq1rk1/ppp1bpp1/4pn1p/3p4/2PP3B/2N1PN2/PP3PPP/R2QKB1R b KQ - 1 7"
    assert position_after_15th_move.context[2].position == "rnbq1rk1/ppp1bpp1/4pn1p/3p2B1/2PP4/2N1PN2/PP3PPP/R2QKB1R w KQ - 0 7"
    assert position_after_15th_move.context[1].position == "rnbq1rk1/ppp1bppp/4pn2/3p2B1/2PP4/2N1PN2/PP3PPP/R2QKB1R b KQ - 0 6"
    assert position_after_15th_move.context[0].position == "rnbq1rk1/ppp1bppp/4pn2/3p2B1/2PP4/2N2N2/PP2PPPP/R2QKB1R w KQ - 5 6"


def test_if_second_position_has_correct_prev_moves_after_board_flipping():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position = positions[1]
    _assert_fens_of_position_sparse_representations_when_flipped(position)


def test_if_10th_position_has_correct_prev_moves_after_board_flipping():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position = positions[11]
    _assert_fens_of_position_sparse_representations_when_flipped(position)


def test_if_18th_position_has_correct_prev_moves_after_board_flipping():
    positions = _load_positions_from_fischer_spassky_1972_game_6(5)
    position = positions[19]
    _assert_fens_of_position_sparse_representations_when_flipped(position)


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
    f = FenTranformation(position.position)
    next_to_move = f.next_to_move()
    transformation = Position2SparseRepresentation(flip_on = next_to_move)
    representation = transformation.transform_position_with_context(position)
    result = None if position.draw() else (position.white_wins())

    if result == None:
        assert representation['result'] == None
    else:
        assert representation['result'] != result

def _load_positions_from_fischer_spassky_1972_game_6(memory_size = 0):
    positions = []
    with PgnReader("tests/test_data/FischerSpassky1972Game6.pgn", memory_size = memory_size) as reader:
        i = iter(reader)
        try:
            while True:
                positions.append(next(i))
        except StopIteration:
            pass
    return positions

def _assert_fens_of_position_sparse_representations_when_flipped(position):
    f = FenTranformation(position.position)
    next_to_move = f.next_to_move()

    transformation = Position2SparseRepresentation(flip_on = next_to_move)
    representation = transformation.transform_position_with_context(position)
    f.flip()
    assert representation['current_position'].fen == f.fen
    for i in range(0, len(representation['prev_positions'])):
        prev_position = representation['prev_positions'][i]
        f = FenTranformation(position.context[i].position)
        f.flip()
        assert prev_position.fen == f.fen
