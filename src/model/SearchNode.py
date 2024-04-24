from ..shared.types import Array1D, Array2D


class SearchNode:
    """Node for the A* search algorithm"""
    def __init__(
            self,
            coordinates: Array1D,
            length_estimate: float,
            parent: "SearchNode" = None,
            piece: Array2D = None,
            goal: Array1D = None
    ):
        self.coordinates = coordinates
        self.parent = parent
        self.length_estimate = length_estimate
        self.piece = piece
        self.goal = goal

    def __str__(self):
        return f"{self.coordinates}, {self.parent.coordinates if self.parent is not None else None}"

    def __lt__(self, other: "SearchNode"):
        return self.length_estimate < other.length_estimate
