from datetime import datetime
import numpy as np
import sys

from src.model.GameField import GameField
from src.playground import is_valid_position, insert_pieces, print_playground, remove_piece, \
    get_neighbour_positions, move_piece_through_maze, add_obstacles


def main():
    obstacles = ([2, 1, 5], [3, 4, 5], [2, 1, 6], [3, 1, 6], [2, 4, 6], [3, 4, 6],)
    piece1_start = np.array([0, 0, 0])
    piece2_start = np.array([4, 0, 0])
    piece3_start = np.array([0, 4, 0])
    piece4_start = np.array([4, 4, 0])

    piece1_goal = np.array([1, 1, 4])
    piece2_goal = np.array([3, 1, 4])
    piece3_goal = np.array([1, 3, 4])
    piece4_goal = np.array([3, 3, 4])

    # todo: extract into function that returns a list of the 4 pieces
    piece1 = np.array([
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
    piece2 = np.array([
        [
            [3, 3],
            [3, 3]
        ],
        [
            [0, 3],
            [0, 0]
        ],
        [
            [0, 3],
            [0, 0],
        ],
        [
            [3, 3],
            [3, 3]
        ]
    ])
    piece3 = np.array([
        [
            [4, 4],
            [4, 4]
        ],
        [
            [0, 0],
            [4, 0]
        ],
        [
            [0, 0],
            [4, 0]
        ],
        [
            [4, 4],
            [4, 4]
        ]
    ])
    piece4 = np.array([
        [
            [5, 5],
            [5, 5]
        ],
        [
            [0, 0],
            [0, 5]
        ],
        [
            [0, 0],
            [0, 5]
        ],
        [
            [5, 5],
            [5, 5]
        ]
    ])

    my_playground = GameField.generate()
    add_obstacles(my_playground, obstacles)
    print_playground(my_playground)
    timestampStart = datetime.now()
    move_piece_through_maze(my_playground,
                            [piece1, piece2, piece3, piece4],
                            [piece1_start, piece2_start, piece3_start, piece4_start],#[:3],
                            [piece1_goal, piece2_goal, piece3_goal, piece4_goal]#[:3]
                            )

    sys.stdout.flush()
    print(my_playground)
    print("search took: ", datetime.now() - timestampStart)


if __name__ == "__main__":
    main()
