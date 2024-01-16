import numpy as np


def generate_playground() -> list[list[int]]:
    playground = [
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [1, 1, 0, 0],
    ]

    return playground


Array2D = np.ndarray
Array1D = np.ndarray


def is_valid_position(playground: Array2D, piece: Array2D, piece_coordinates: Array1D) -> bool:
    piece_x, piece_y = piece_coordinates
    dim_y, dim_x = piece.shape
    piece_dest = playground[piece_y:piece_y + dim_y, piece_x: piece_x + dim_x]

    return (piece_dest * piece).max() == 0 


def insert_piece(playground, piece, piece_coordinates) -> None:
    for row_index in range(len(piece)):
        for col_index in range(len(piece[row_index])):
            is_not_requested = piece[row_index][col_index] == 0
            if is_not_requested:
                continue

            playground[row_index + piece_coordinates[1]][col_index + piece_coordinates[0]] = piece[row_index][col_index]


def print_playground(playground) -> None:
    for row in playground:
        print(row)
