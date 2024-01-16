from src.playground import is_valid_position


def test_is_valid_position_basic():
    playground1 = [
        [0]
    ]

    playground1_occupied = [
        [1]
    ]

    piece1 = [
        [2]
    ]

    assert is_valid_position(playground1, piece1, [0, 0])
    assert not is_valid_position(playground1_occupied, piece1, [0, 0])


def test_is_valid_position_advanced():
    playground2 = [
        [0, 1, 0],
        [0, 0, 0]
    ]

    piece_l = [
        [2, 0],
        [2, 2]
    ]

    assert is_valid_position(playground2, piece_l, [0, 0])
    assert not is_valid_position(playground2, piece_l, [1, 0])
