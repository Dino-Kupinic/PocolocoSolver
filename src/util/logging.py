from ..shared.types import Array2D


def print_game_field(game_field: Array2D) -> None:
    """Prints the game field in the console"""
    print()
    for row in game_field:
        print(row)
