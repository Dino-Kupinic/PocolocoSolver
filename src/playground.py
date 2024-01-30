from typing import Final

import numpy as np
import queue

type Array2D = np.ndarray
type Array1D = np.ndarray

CUBE_BORDER: Final[int] = 9
"""
Represents the border of the poco loco. Used for "out of bound" checks
"""
OCCUPIED_FIELD: Final[int] = 1
"""
Represents a field in which a cube resides.
"""
EMPTY_FIELD: Final[int] = 0
"""
Represents an empty field in which a cube can move into
"""


def generate_playground() -> Array2D:
    playground = np.array([
        [9, 9, 9, 9, 9, 9],
        [9, 0, 0, 1, 1, 9],
        [9, 0, 0, 0, 1, 9],
        [9, 1, 0, 0, 0, 9],
        [9, 1, 1, 0, 0, 9],
        [9, 9, 9, 9, 9, 9]
    ])

    return playground


def get_piece_dest(playground: Array2D, piece: Array2D, piece_coordinates: Array1D) -> Array2D:
    piece_x, piece_y = piece_coordinates
    dim_y, dim_x = piece.shape
    size_y, size_x = playground.shape

    valid_x_pos = 0 <= piece_x <= size_x - dim_x
    valid_y_pos = 0 <= piece_y <= size_y - dim_y
    assert valid_x_pos and valid_y_pos, f"Invalid piece coordinates: {piece_x}, {piece_y}"

    piece_dest = playground[piece_y:piece_y + dim_y, piece_x: piece_x + dim_x]
    return piece_dest


# this solution only delivers coordinates where there are only clear fields and doesn't take pieces into consideration
def is_valid_position(playground: Array2D, piece: Array2D, piece_coordinates: Array1D) -> bool:
    piece_dest = get_piece_dest(playground, piece, piece_coordinates)

    return (piece_dest * piece).max() == 0


def insert_piece(playground: Array2D, piece: Array2D, piece_coordinates: Array1D) -> None:
    piece_dest = get_piece_dest(playground, piece, piece_coordinates)

    piece_dest += piece


def print_playground(playground) -> None:
    print()
    for row in playground:
        print(row)


def remove_piece(playground: Array2D, piece: Array2D, piece_coordinates: Array1D) -> None:
    piece_dest = get_piece_dest(playground, piece, piece_coordinates)
    piece_dest -= piece


def get_neighbour_positions(piece_coordinates: Array1D) -> list[Array1D]:
    for offset in ([0, 1], [1, 0], [0, -1], [-1, 0]):
        yield piece_coordinates + offset


def move_piece_through_maze(
        playground: Array2D,
        piece: Array2D,
        piece_coordinates: Array1D,
        piece_goal: Array1D,
) -> None:
    checked_coordinates = set()

    next_to_visit = queue.Queue()
    next_to_visit.put(piece_coordinates)

    while not next_to_visit.empty():
        current_coordinate = next_to_visit.get()
        print(current_coordinate)

        if np.array_equal(current_coordinate, piece_goal):
            insert_piece(playground, piece, current_coordinate)
            print('Das Piece ist an der richtigen Stelle', current_coordinate)
            print_playground(playground)
            break
        else:
            pass
            # print(runs)

        for neighbour in get_neighbour_positions(current_coordinate):
            if tuple(neighbour) not in checked_coordinates:
                if is_valid_position(playground, piece, neighbour):
                    next_to_visit.put(neighbour)

        checked_coordinates.add(tuple(current_coordinate))
