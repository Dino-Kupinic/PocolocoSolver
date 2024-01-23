import numpy as np

from src.playground import generate_playground, is_valid_position, insert_piece, print_playground, remove_piece, \
    move_piece_through_maze


def main():
    piece_coordinates = np.array([1, 1])

    piece_goal = np.array([3, 3])

    piece_l = np.array([
        [2, 0],
        [2, 2]
    ])

    piece_j = np.array([
        [0, 0],
        [2, 2]
    ])

    my_playground = generate_playground()
    # if is_valid_position(my_playground, piece_l, piece_coordinates):
    #     insert_piece(my_playground, piece_l, piece_coordinates)
    #     move_piece_through_maze(my_playground, piece_l, piece_coordinates, piece_goal)
    # else:
    #     print("Invalid position")

    move_piece_through_maze(my_playground, piece_j, piece_coordinates, piece_goal)


if __name__ == "__main__":
    main()
