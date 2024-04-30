from ..shared.types import Array2D


class SearchNode:
    def __init__(self, coordinates: Array2D, length_estimate: float, parent: "SearchNode" = None):
        self.coordinates = coordinates
        self.parent = parent
        self.length_estimate = length_estimate

    def __str__(self):
        return f"{self.coordinates}, {self.parent.coordinates if self.parent is not None else None}"

    def __lt__(self, other: "SearchNode"):
        return self.length_estimate < other.length_estimate
