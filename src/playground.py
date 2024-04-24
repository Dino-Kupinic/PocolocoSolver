import heapq

from src.model.SearchNode import SearchNode

from shared.types import Array1D, Array2D, np
from src.util.logging import print_game_field


def get_piece_dest(playground: Array2D, piece: Array2D, piece_coordinates: Array1D) -> Array2D:
    piece_x, piece_y = piece_coordinates
    dim_y, dim_x = piece.shape
    size_y, size_x = playground.shape

    valid_x_pos = 0 <= piece_x <= size_x - dim_x
    valid_y_pos = 0 <= piece_y <= size_y - dim_y
    assert valid_x_pos and valid_y_pos, f"Invalid piece coordinates: {piece_x}, {piece_y}"

    piece_dest = playground[piece_y:piece_y + dim_y, piece_x: piece_x + dim_x]
    return piece_dest


# this solution only delivers coordinates where there are only clear fields and doesn't take pieces into consideration
def is_valid_position(playground: Array2D, piece: Array2D, piece_coordinates: Array1D) -> bool:
    piece_dest = get_piece_dest(playground, piece, piece_coordinates)

    return (piece_dest * piece).max() == 0


def insert_piece(playground: Array2D, piece: Array2D, piece_coordinates: Array1D) -> None:
    piece_dest = get_piece_dest(playground, piece, piece_coordinates)

    piece_dest += piece


def remove_piece(playground: Array2D, piece: Array2D, piece_coordinates: Array1D) -> None:
    piece_dest = get_piece_dest(playground, piece, piece_coordinates)
    piece_dest -= piece


def get_neighbour_positions(piece_coordinates: Array1D) -> list[Array1D]:
    for offset in ([0, 1], [1, 0], [0, -1], [-1, 0]):
        yield piece_coordinates + offset


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


def calc_lower_bound_distance(piece_coords1: list[Array1D], piece_coords2: list[Array1D]) -> float:
    sum_pieces = 0.0
    for i in range(len(piece_coords1)):
        sum_pieces += abs(piece_coords1[i][0] - piece_coords2[i][0])
    return sum_pieces

def move_piece_through_maze(
        game_field: Array2D,
        pieces: list[Array2D],
        piece_start_positions: list[Array1D],
        piece_goals: list[Array1D],
) -> None:
    checked_coordinates = set()

    next_to_visit = []

    lower_bound_distance = calc_lower_bound_distance(piece_start_positions, piece_goals)
    for index in range(len(piece_start_positions)):
        heapq.heappush(next_to_visit,
                       (SearchNode(piece_start_positions[index], lower_bound_distance, piece=pieces[index], goal=piece_goals[index])))

    while len(next_to_visit) > 0:
        current_node: SearchNode = heapq.heappop(next_to_visit)

        print(current_node)

        if np.array_equal(current_node.coordinates, current_node.goal):
            insert_piece(game_field, current_node.piece, current_node.coordinates)
            print('Das Piece ist an der richtigen Stelle', current_node)
            print_game_field(game_field)
            print_path(current_node)
            break

        for neighbour in get_neighbour_positions(current_node.coordinates):
            if tuple(neighbour) not in checked_coordinates:
                if is_valid_position(game_field, current_node.piece, neighbour):
                    lower_bound_distance_neighbour = calc_lower_bound_distance([neighbour], [current_node.goal]) \
                                                     + len(get_path_rec(current_node))
                    heapq.heappush(next_to_visit,
                                   SearchNode(neighbour, lower_bound_distance_neighbour, current_node, current_node.piece, current_node.goal)
                                   )
        checked_coordinates.add(tuple(current_node.coordinates))
