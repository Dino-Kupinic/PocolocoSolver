import numpy as np

from src.playground import generate_playground, is_valid_position, insert_piece, print_playground, remove_piece, \
    get_neighbour_positions, move_piece_through_maze, add_obstacles


def main():
    piece_coordinates = np.array([0, 0, 0])

    piece_goal = np.array([1, 1, 4])

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

    my_playground = generate_playground()
    add_obstacles(my_playground, ([2, 1, 5], [2, 1, 6], [3, 1, 6]))
    print_playground(my_playground)
    move_piece_through_maze(my_playground, piece_test, piece_coordinates, piece_goal)

if __name__ == "__main__":
    main()
