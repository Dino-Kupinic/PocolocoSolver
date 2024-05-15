from ..shared.globals import CB, EF, OF
from ..shared.types import Array2D, Array3D, np


class GameField:
    """Class representing the game field of poco loco"""

    @staticmethod
    def generate() -> Array2D:
        """Generate the game field"""
        field: Array3D = np.zeros((10, 6, 6))
        layer = [
            [CB, CB, CB, CB, CB, CB],
            [CB, EF, EF, EF, EF, CB],
            [CB, EF, EF, EF, EF, CB],
            [CB, EF, EF, EF, EF, CB],
            [CB, EF, EF, EF, EF, CB],
            [CB, CB, CB, CB, CB, CB]
        ]
        for i in range(4, 10):
            field[i, :, :] += layer

        return field

