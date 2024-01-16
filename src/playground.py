def generate_playground() -> list[list[int]]:
    playground = [
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [1, 1, 0, 0],
    ]

    return playground


def is_valid_position(playground, piece, piece_coordinates) -> bool:
    for row_index in range(len(piece)):
        for col_index in range(len(piece[row_index])):
            is_occupied = playground[row_index + piece_coordinates[1]][col_index + piece_coordinates[0]] == 1
            is_requested = piece[row_index][col_index] == 2

            if is_occupied and is_requested:
                return False

    return True


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
