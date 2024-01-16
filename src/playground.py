import numpy as np

Array2D = np.ndarray
Array1D = np.ndarray


def generate_playground() -> Array2D:
    playground = np.array([
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [1, 1, 0, 0],
    ])

    return playground


def get_piece_dest(piece, piece_coordinates, playground):
    piece_x, piece_y = piece_coordinates
    dim_y, dim_x = piece.shape
    piece_dest = playground[piece_y:piece_y + dim_y, piece_x: piece_x + dim_x]
    return piece_dest


def is_valid_position(playground: Array2D, piece: Array2D, piece_coordinates: Array1D) -> bool:
    piece_dest = get_piece_dest(piece, piece_coordinates, playground)

    return (piece_dest * piece).max() == 0


def insert_piece(playground: Array2D, piece: Array2D, piece_coordinates: Array1D) -> None:
    piece_dest = get_piece_dest(piece, piece_coordinates, playground)

    piece_dest += piece


def print_playground(playground) -> None:
    for row in playground:
        print(row)
