import numpy as np

from src.model.GameField import GameField
from src.playground import is_valid_position, insert_pieces, print_playground, remove_piece, \
    get_neighbour_positions, move_piece_through_maze, add_obstacles


def main():
    obstacles = ([2, 1, 5], [3, 4, 5], [2, 1, 6], [3, 1, 6], [2, 4, 6], [3, 4, 6],)
    piece_coordinates = np.array([0, 0, 0])

    piece_goal = np.array([1, 1, 4])

    # todo: extract into function that returns a list of the 4 pieces
    piece_test = np.array([
        [
            [2, 2],
            [2, 2]
        ],
        [
            [2, 0],
            [0, 0]
        ],
        [
            [2, 0],
            [0, 0],
        ],
        [
            [2, 2],
            [2, 2]
        ]
    ])

    my_playground = GameField.generate()
    add_obstacles(my_playground, obstacles)
    print_playground(my_playground)
    move_piece_through_maze(my_playground, piece_test, piece_coordinates, piece_goal)


if __name__ == "__main__":
    main()
