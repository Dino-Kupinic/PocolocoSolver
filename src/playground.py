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
def is_valid_position(playground: Array3D, pieces: list[Array3D], pieces_coordinates: Array2D) -> bool:
    playground_copy = playground.copy()
    for piece, piece_coordinates in zip(pieces, pieces_coordinates):
        piece_dest = get_piece_dest(playground_copy, piece, piece_coordinates)
        if (piece_dest * piece).max() != 0: return False
        piece_dest[:] = piece
    return True


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


def get_neighbour_positions(pieces_coordinates: Array2D) -> list[Array2D]:
    for piece_index in range(len(pieces_coordinates)):
        for offset in ([0, 0, 1], [0, 0, -1], [0, 1, 0], [0, -1, 0], [1, 0, 0], [-1, 0, 0]):
            neighbour_coordinates = pieces_coordinates[piece_index] + offset
            if min(neighbour_coordinates) < 0:
                continue
            if max(neighbour_coordinates[:2]) > 4 or neighbour_coordinates[2] > 6:
                continue
            neighbouring_coordinates = pieces_coordinates.copy()
            neighbouring_coordinates[piece_index] = neighbour_coordinates
            yield neighbouring_coordinates


def print_path(node: SearchNode):
    print("Path: ", end="")
    path = get_path_rec(node)
    if len(path) <= 10:
        print(", ".join(map(str, path)))
    else:
        print("\n  ", "\n  ".join(map(str, path)))


def get_path_rec(node: SearchNode) -> list[Array1D]:
    path = []
    if node.parent is not None:
        path = get_path_rec(node.parent)
    path.append(node.coordinates)
    return path


def calc_lower_bound_distance(pieces_coords1: list[Array2D], pieces_coords2: list[Array2D]) -> float:
    return sum(np.sum(np.abs(piece_coords1 - piece_coords2)) for piece_coords1,piece_coords2 in zip(pieces_coords1,pieces_coords2))


def freeze(mat: Array2D) -> tuple[tuple[float]]:
    return tuple(tuple(row) for row in mat)


def generate_json(node: SearchNode):
    path = get_path_rec(node)
    pieces = []
    for index, coordinates in enumerate(path):
        coordinates = list(coordinates)
        piece = {
            "name": "piece",
            "coordinates": {
                "x": int(coordinates[0]),
                "y": int(coordinates[1]),
                "z": int(coordinates[2])
            }
        }
        pieces.append(piece)
    output = {"pieces": pieces}
    print('output')
    print(output)
    with open("sample.json", "w") as outfile:
        json.dump(output, outfile)


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

    searchNodeCnt = 0
    while len(next_to_visit) > 0:
        current_node = heapq.heappop(next_to_visit)
        searchNodeCnt += 1
        print(f"\r{searchNodeCnt}: {current_node.length_estimate}, {len(next_to_visit)}", end='')
        #print(current_node)

        if np.array_equal(current_node.coordinates, piece_goal):
            insert_pieces(playground, pieces, current_node.coordinates)
            print('\nDas Piece ist an der richtigen Stelle!', current_node)
            print_path(current_node)
            generate_json(current_node)
            break

        for neighbour in get_neighbour_positions(current_node.coordinates):
            if freeze(neighbour) not in checked_coordinates:
                if is_valid_position(playground, pieces, neighbour):
                    lower_bound_distance_neighbour = calc_lower_bound_distance(neighbour, piece_goal) \
                                                     + len(get_path_rec(current_node))
                    heapq.heappush(next_to_visit,
                                   SearchNode(neighbour, lower_bound_distance_neighbour, current_node)
                                   )
        checked_coordinates.add(freeze(current_node.coordinates))
