import heapq

from src.model.SearchNode import SearchNode
from shared.types import Array1D, Array2D, Array3D, np


def add_obstacles(playground: Array3D, obstacles: list[Array1D]):
    for obstacle in obstacles:
        playground[obstacle[2], obstacle[1], obstacle[0]] = 1

    return playground


def get_piece_dest(playground: Array3D, piece: Array3D, piece_coordinates: Array1D) -> Array3D:
    piece_x, piece_y, piece_z = piece_coordinates
    dim_z, dim_y, dim_x = piece.shape
    size_z, size_y, size_x = playground.shape

    valid_x_pos = 0 <= piece_x <= size_x - dim_x
    valid_y_pos = 0 <= piece_y <= size_y - dim_y
    valid_z_pos = 0 <= piece_z <= size_z - dim_z
    assert valid_x_pos and valid_y_pos and valid_z_pos, f"Invalid piece coordinates: {piece_x}, {piece_y}, {piece_z}"

    piece_dest = playground[piece_z:piece_z + dim_z, piece_y:piece_y + dim_y, piece_x: piece_x + dim_x]
    return piece_dest


# this solution only delivers coordinates where there are only clear fields and doesn't take pieces into consideration
def is_valid_position(playground: Array3D, piece: Array3D, piece_coordinates: Array1D) -> bool:
    piece_dest = get_piece_dest(playground, piece, piece_coordinates)

    return (piece_dest * piece).max() == 0


def insert_pieces(playground: Array3D, pieces: list[Array3D], piece_coordinates: Array2D) -> None:
    for piece, piece_coordinates in zip(pieces, piece_coordinates):
        piece_dest = get_piece_dest(playground, piece, piece_coordinates)
        piece_dest += piece


def print_playground(playground) -> None:
    print()
    for layer in playground:
        for row in layer:
            print(row)
        print()


def remove_piece(playground: Array3D, piece: Array3D, piece_coordinates: Array1D) -> None:
    piece_dest = get_piece_dest(playground, piece, piece_coordinates)
    piece_dest -= piece


def get_neighbour_positions(piece_coordinates: Array1D) -> list[Array1D]:
    for offset in ([0, 0, 1], [0, 0, -1], [0, 1, 0], [0, -1, 0], [1, 0, 0], [-1, 0, 0]):
        neighbour_coordinates = piece_coordinates + offset
        if min(neighbour_coordinates) < 0:
            continue
        if max(neighbour_coordinates[:2]) > 4 or neighbour_coordinates[2] > 6:
            continue
        yield neighbour_coordinates


def print_path(node: SearchNode):
    print("Path: ", end="")
    path = get_path_rec(node)
    print(", ".join(map(str, path)))


def get_path_rec(node: SearchNode) -> list[Array1D]:
    path = []
    if node.parent is not None:
        path = get_path_rec(node.parent)
    path.append(node.coordinates)
    return path


def calc_lower_bound_distance(piece_coords1: Array2D, piece_coords2: Array2D) -> float:
    return np.sum(np.abs(piece_coords1 - piece_coords2))


def move_piece_through_maze(
        playground: Array3D,
        pieces: list[Array3D],
        piece_start: Array2D,
        piece_goal: Array2D
) -> None:
    checked_coordinates = set()

    next_to_visit = []

    lower_bound_distance = calc_lower_bound_distance(piece_start, piece_goal)
    heapq.heappush(next_to_visit, SearchNode(piece_start, lower_bound_distance))

    while len(next_to_visit) > 0:
        current_node = heapq.heappop(next_to_visit)
        print(current_node)

        if np.array_equal(current_node.coordinates, piece_goal):
            insert_pieces(playground, pieces, current_node.coordinates)
            print('Das Piece ist an der richtigen Stelle!', current_node)
            print_path(current_node)
            break

        for neighbour in get_neighbour_positions(current_node.coordinates):
            if tuple(neighbour) not in checked_coordinates:
                if is_valid_position(playground, pieces, neighbour):
                    lower_bound_distance_neighbour = calc_lower_bound_distance(neighbour, piece_goal) \
                                                     + len(get_path_rec(current_node))
                    heapq.heappush(next_to_visit,
                                   SearchNode(neighbour, lower_bound_distance_neighbour, current_node)
                                   )
        checked_coordinates.add(tuple(current_node.coordinates))
