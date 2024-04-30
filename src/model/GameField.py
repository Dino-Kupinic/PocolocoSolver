from ..shared.globals import CB, EF, OF
from ..shared.types import Array2D, np


class GameField:
    """Class representing the game field of poco loco"""

    @staticmethod
    def generate() -> Array2D:
        """Generate a game field"""
        return np.array([
            [CB, CB, CB, CB, CB, CB],
            [CB, EF, EF, EF, OF, CB],
            [CB, EF, EF, EF, EF, CB],
            [CB, EF, EF, EF, EF, CB],
            [CB, OF, EF, EF, EF, CB],
            [CB, CB, CB, CB, CB, CB]
        ])

