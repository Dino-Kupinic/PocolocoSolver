import numpy as np

from src.playground import is_valid_position, insert_piece


def test_is_valid_position_basic():
    playground1 = np.array([
        [0]
    ])

    playground1_occupied = np.array([
        [1]
    ])

    piece1 = np.array([
        [2]
    ])

    assert is_valid_position(playground1, piece1, np.array([0, 0]))
    assert not is_valid_position(playground1_occupied, piece1, np.array([0, 0]))


def test_is_valid_position_advanced():
    playground2 = [
        [0, 1, 0],
        [0, 0, 0]
    ]

    piece_l = np.array([
        [2, 0],
        [2, 2]
    ])

    assert is_valid_position(playground2, piece_l, np.array([0, 0]))
    assert not is_valid_position(playground2, piece_l, np.array([1, 0]))


def test_insert_piece_advanced():
    playground2 = np.array([
        [0, 1, 0],
        [0, 0, 0]
    ])

    piece_l = np.array([
        [2, 0],
        [2, 2]
    ])

    insert_piece(playground2, piece_l, np.array([0, 0]))

    playground2_expected = np.array([
        [2, 1, 0],
        [2, 2, 0]
    ])

    assert (playground2 == playground2_expected).all()
