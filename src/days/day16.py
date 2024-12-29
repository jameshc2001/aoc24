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

#end can be reached from multiple directions

def part01(input):
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
    ignored = 0
    for pos in positions:
        has_left = add_direction(pos, (-1, 0)) in positions
        has_right = add_direction(pos, (1, 0)) in positions
        has_up = add_direction(pos, (0, -1)) in positions
        has_down = add_direction(pos, (0, 1)) in positions
        if (has_left and has_right and not has_up and not has_down):
            ignored += 1
            continue #ignore left-right tiles
        if (has_up and has_down and not has_left and not has_right):
            ignored += 1
            continue #ignore up-down tiles
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
    
    for v, a in neighbours_and_cost.items():
        assert v in vertices
        for n, _ in a:
            assert n in vertices
    
    dist, _ = big_dijkstra(vertices, neighbours_and_cost, Vertex(start_position, (1, 0)))
    return min([dist[v] for v in vertices if v.position == end_position])

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
                prev[v] = u
    
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
        sys.setrecursionlimit(10000)
        assert 98416 == part01(f.read())

def test_part02_sample():
    assert 64 == part02(sample)