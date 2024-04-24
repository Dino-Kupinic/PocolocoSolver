class Piece:
    """Class representing a piece. The game has a total of 4 pieces."""
    _cubes = None

    def __init__(self, cubes):
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
