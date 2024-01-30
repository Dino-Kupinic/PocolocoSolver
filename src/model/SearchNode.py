import numpy as np

type Array1D = np.ndarray


class SearchNode:
    def __init__(self, coordinates: Array1D, parent: "SearchNode" = None):
        self.coordinates = coordinates
        self.parent = parent

    def __str__(self):
        return f"{self.coordinates}, {self.parent.coordinates if self.parent is not None else None}"
