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


def move_piece_through_maze(
        playground: Array2D,
        piece: Array2D,
        piece_coordinates: Array1D,
        piece_goal: Array1D,
) -> None:
    piece_coordinates_before = piece_coordinates.copy()

    checked_coordinates = list()

    next_to_visit = queue.Queue()
    next_to_visit.put(piece_coordinates)

    '''while piece_coordinates is not piece_goal:
        if not is_valid_position(playground, piece, piece_coordinates_before):
            remove_piece(playground, piece, piece_coordinates_before)

        if is_valid_position(playground, piece, piece_coordinates):
            insert_piece(playground, piece, piece_coordinates)
            piece_coordinates_before = piece_coordinates.copy()

            piece_coordinates += [1, 0]

        else:
            piece_coordinates[0] = 0
            piece_coordinates += [0, 1]

        print_playground(playground)'''
    runs = 0
    while not next_to_visit.empty():
        runs += 1
        current_coordinate = next_to_visit.get()

        if np.array_equal(current_coordinate, piece_goal):
            insert_piece(playground, piece, current_coordinate)
            print('Das Piece ist an der richtigen Stelle', current_coordinate)
            print_playground(playground)
            break
        else:
            print(runs)

        if is_valid_position(playground, piece, current_coordinate - [1, 0]):
            next_to_visit.put(current_coordinate - [1, 0])

        if is_valid_position(playground, piece, current_coordinate + [1, 0]):
            next_to_visit.put(current_coordinate + [1, 0])

        if is_valid_position(playground, piece, current_coordinate + [0, 1]):
            next_to_visit.put(current_coordinate + [0, 1])

        if is_valid_position(playground, piece, current_coordinate - [0, 1]):
            next_to_visit.put(current_coordinate - [0, 1])

        checked_coordinates.append(current_coordinate)