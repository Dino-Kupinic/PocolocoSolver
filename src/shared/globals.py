from typing import Final

# Game Field

CB: Final[int] = 9
"""'Cube Border', Represents the border of the poco loco. Used for "out of bound" checks"""
OF: Final[int] = 1
"""'Occupied Field', Represents a field in which a cube resides."""
EF: Final[int] = 0
"""'Empty Field', Represents an empty field in which a cube can move into"""

# Logging
log_format: Final[str] = '%(asctime)s - %(message)s'
