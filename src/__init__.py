import numpy as np

from src.playground import generate_playground, is_valid_position, insert_piece, print_playground


def main():
    piece_coordinates = np.array([1, 0])

    piece_l = np.array([
        [2, 0],
        [2, 2]
    ])

    my_playground = generate_playground()
    if is_valid_position(my_playground, piece_l, piece_coordinates):
        insert_piece(my_playground, piece_l, piece_coordinates)
        print_playground(my_playground)
    else:
        print("Invalid position")


if __name__ == "__main__":
    main()
