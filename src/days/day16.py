import sys
import heapq
from collections import defaultdict

class Vertex():
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
    
    def __hash__(self):
        return hash((self.position, self.direction))

    def __eq__(self, value):
        return self.position == value.position and self.direction == value.direction

    def __repr__(self):
        return "pos" + str(self.position) + ", dir" + str(self.direction)

def part01(input):
    start_position, end_position, vertices, neighbours_and_cost = get_graph_parameters(input)
    dist, _ = big_dijkstra(vertices, neighbours_and_cost, Vertex(start_position, (1, 0)))
    return min([dist[v] for v in vertices if v.position == end_position])

def part02(input):
    start_position, end_position, vertices, neighbours_and_cost = get_graph_parameters(input)
    dist, prev = big_dijkstra(vertices, neighbours_and_cost, Vertex(start_position, (1, 0)))

    min_dist = min([dist[v] for v in vertices if v.position == end_position])
    to_explore = [v for v in vertices if v.position == end_position and dist[v] == min_dist]
    best_tiles = set()
    while (len(to_explore) > 0):
        u = to_explore.pop()
        best_tiles.add(u.position)
        next_vertices = prev[u]
        for v in next_vertices:
            if (v.position != u.position): #add tiles from v to u
                forwards = v.position
                while (forwards != u.position):
                    forwards = add_direction(forwards, v.direction)
                    best_tiles.add(forwards)
            to_explore.append(v)

    return len(best_tiles)

def get_graph_parameters(input):
    positions = set()
    start_position = None
    end_position = None
    for y, line in enumerate(input.split("\n")):
        for x, character in enumerate(line):
            pos = (x, y)
            if (character != '#'): positions.add(pos)
            if (character == 'S'): start_position = pos
            elif (character == 'E'): end_position = pos
    
    vertices = set()
    for pos in positions:
        has_left = add_direction(pos, (-1, 0)) in positions
        has_right = add_direction(pos, (1, 0)) in positions
        has_up = add_direction(pos, (0, -1)) in positions
        has_down = add_direction(pos, (0, 1)) in positions
        if (has_left and has_right and not has_up and not has_down): continue #ignore left-right tiles
        if (has_up and has_down and not has_left and not has_right): continue #ignore up-down tiles
        vertices.add(Vertex(pos, (1, 0)))
        vertices.add(Vertex(pos, (0, 1)))
        vertices.add(Vertex(pos, (-1, 0)))
        vertices.add(Vertex(pos, (0, -1)))

    neighbours_and_cost = defaultdict(list)
    for v in vertices:
        neighbours_and_cost[v].append((Vertex(v.position, rotate_clockwise(v.direction)), 1000))
        neighbours_and_cost[v].append((Vertex(v.position, rotate_counter_clockwise(v.direction)), 1000))
        if (add_direction(v.position, v.direction) not in positions): continue #facing wall

        forward_cost = 1
        forward_position = add_direction(v.position, v.direction)
        while (Vertex(forward_position, v.direction) not in vertices):
            forward_position = add_direction(forward_position, v.direction)
            forward_cost += 1
        neighbours_and_cost[v].append((Vertex(forward_position, v.direction), forward_cost))
    neighbours_and_cost = dict(neighbours_and_cost)
    return start_position,end_position,vertices,neighbours_and_cost

def big_dijkstra(vertices, neighbours_and_cost, start):
    dist = {}
    prev = {}
    Q = set()
    for v in vertices:
        dist[v] = sys.maxsize
        Q.add(v)
    dist[start] = 0
    prev[start] = []

    while (len(Q) > 0):
        u = min(Q, key=lambda pos: dist[pos])
        Q.remove(u)

        for v, cost in neighbours_and_cost[u]:
            alt = dist[u] + cost
            if (alt < dist[v]):
                dist[v] = alt
                prev[v] = [u]
            elif (alt == dist[v]): prev[v].append(u)
    
    return dist, prev

def get_neighbours_with_cost(u, Q):
    next = Vertex(add_direction(u.position, u.direction), u.direction)
    clockwise = Vertex(u.position, rotate_clockwise(u.direction))
    counter_clockwise = Vertex(u.position, rotate_counter_clockwise(u.direction))

    neighbours_with_cost = []
    if (next in Q): neighbours_with_cost.append((next, 1))
    if (clockwise in Q): neighbours_with_cost.append((clockwise, 1000))
    if (counter_clockwise in Q): neighbours_with_cost.append((counter_clockwise, 1000))

    return neighbours_with_cost

def add_direction(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])

def rotate_counter_clockwise(direction):
    new_direction = rotate_clockwise(direction)
    return (-new_direction[0], -new_direction[1])

def rotate_clockwise(direction):
    if (direction == (1, 0)): return (0, 1)
    if (direction == (0, 1)): return (-1, 0)
    if (direction == (-1, 0)): return (0, -1)
    if (direction == (0, -1)): return (1, 0)

#TESTS

sample = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

def test_part01_sample():
    assert 11048 == part01(sample)

def test_part01_input():
    with open("src/inputs/day16.txt", "r") as f:
        assert 98416 == part01(f.read())

def test_part02_sample():
    assert 64 == part02(sample)

def test_part02_input():
    with open("src/inputs/day16.txt", "r") as f:
        assert 471 == part02(f.read())