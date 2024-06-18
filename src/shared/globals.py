from typing import Final

import numpy as np

# Game Field

CB: Final[int] = 9
"""'Cube Border', Represents the border of the poco loco. Used for "out of bound" checks"""
OF: Final[int] = 1
"""'Occupied Field', Represents a field in which a cube resides."""
EF: Final[int] = 0
"""'Empty Field', Represents an empty field in which a cube can move into"""

# Logging
log_format: Final[str] = '%(asctime)s - %(message)s'

# Pieces Coordinates
piece1_start = np.array([0, 0, 0])
piece2_start = np.array([4, 0, 0])
piece3_start = np.array([0, 4, 0])
piece4_start = np.array([4, 4, 0])

piece1_goal = np.array([1, 1, 4])
piece2_goal = np.array([3, 1, 4])
piece3_goal = np.array([1, 3, 4])
piece4_goal = np.array([3, 3, 4])
