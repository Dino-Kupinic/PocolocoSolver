from src.model.Cube import Cube


class Piece:
    _cubes: list[Cube] = None

    def __init__(self, cubes: list[Cube]):
        self._cubes = cubes

    @classmethod
    def move(cls):
        pass

    @classmethod
    def __str__(cls):
        """
        String representation of the piece
        """
        print(cls._cubes)
