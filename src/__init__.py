import numpy as np
import logging


from src.model.GameField import GameField
from src.playground import is_valid_position, insert_piece, print_game_field, remove_piece, \
    move_piece_through_maze
from src.shared.globals import log_format

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(filename="logfile.log", level=logging.INFO, format=log_format)
    logger.info("Started")

    piece_coordinates_l = np.array([1, 1])

    piece_goal_l = np.array([3, 3])

    piece_l = np.array([
        [2, 0],
        [2, 2]
    ])

    # border rows and columns may not be empty
    piece_coordinates_j = np.array([2, 1])
    piece_goal_j = np.array([3, 2])
    piece_j = np.array([
        [2, 2],
        [0, 2]
    ])

    my_playground = GameField.generate()
    # if is_valid_position(my_playground, piece_l, piece_coordinates):
    #     insert_piece(my_playground, piece_l, piece_coordinates)
    #     move_piece_through_maze(my_playground, piece_l, piece_coordinates, piece_goal)
    # else:
    #     print("Invalid position")

    move_piece_through_maze(my_playground, [piece_l, piece_j], [piece_coordinates_l, piece_coordinates_j], [piece_goal_l, piece_goal_j])
    logger.info('Finished')


if __name__ == "__main__":
    main()
